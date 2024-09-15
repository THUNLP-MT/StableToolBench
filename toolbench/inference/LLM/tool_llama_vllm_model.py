# import os

from openai import OpenAI
# import httpx
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import time
# import json
import traceback
from toolbench.utils import process_system_message
from toolbench.model.model_adapter import get_conversation_template
from toolbench.inference.utils import react_parser
import string, random, json

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def completion_request(key, base_url, prompt,
                        model="ToolBench/ToolLLaMA-2-7b-v2", process_id=0, **args):
    json_data = {
        "model": model,
        "prompt": prompt,
        "temperature": 0,
        "max_tokens": 1024,
        "stop": "</s>",
        "echo": False,
        "extra_body": {
            "truncate_prompt_tokens": 7168, # 7680
        },
        **args
    }

    try:
        client = OpenAI(base_url=base_url, api_key=key)
        vllm_response = client.completions.create(**json_data)
        json_data = vllm_response.dict()
        return json_data

    except Exception as e:
        print("Unable to generate ChatCompletion response")
        traceback.print_exc()
        import pdb;  pdb.set_trace()
        return {"error": str(e), "total_tokens": 0}

class ToolLLaMA_vllm:
    def __init__(
            self, 
            model="ToolBench/ToolLLaMA-2-7b-v2", 
            template:str="tool-llama-single-round",
            openai_key="", 
            base_url=None
            ):
        self.model = model
        self.template = template
        self.conversation_history = []
        self.openai_key = openai_key
        self.base_url = base_url
        self.time = time.time()
        self.TRY_TIME = 6

    def add_message(self, message):
        self.conversation_history.append(message)

    def change_messages(self, messages):
        self.conversation_history = messages

    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        print("before_print" + "*" * 50)
        for message in self.conversation_history:
            print_obj = f"{message['role']}: {message['content']} "
            if "function_call" in message.keys():
                print_obj = print_obj + f"function_call: {message['function_call']}"
            # if 'tool_calls' in message.keys():
            #     print_obj = print_obj + f"tool_calls: {message['tool_calls']}"
            #     print_obj = print_obj + f"number of tool calls: {len(message['tool_calls'])}"
            # if detailed:
            #     print_obj = print_obj + f"function_call: {message['function_call']}"
            #     print_obj = print_obj + f"tool_calls: {message['tool_calls']}"
            #     print_obj = print_obj + f"function_call_id: {message['function_call_id']}"
            print_obj += ""
            print(
                colored(
                    print_obj,
                    role_to_color[message["role"]],
                )
            )
        print("end_print" + "*" * 50)

    def parse(self, tools, process_id, **args):
        conv = get_conversation_template(self.template)
        if self.template == "tool-llama":
            roles = {"human": conv.roles[0], "gpt": conv.roles[1]}
        elif self.template == "tool-llama-single-round" or self.template == "tool-llama-multi-rounds":
            roles = {"system": conv.roles[0], "user": conv.roles[1], "tool": conv.roles[2], "assistant": conv.roles[3]}

        self.time = time.time()
        if tools != []:
            functions = [tool['function'] for tool in tools]
        conversation_history = self.conversation_history
        for _ in range(self.TRY_TIME):
            if _ != 0:
                time.sleep(15)
            prompt = ''
            for message in conversation_history:
                role = roles[message['role']]
                content = message['content']
                if role == "System" and tools != []:
                    content = process_system_message(content, functions)
                # if role == "Assistant":
                #     content = react_deparser(message['content'], message['tool_calls'][0]['function']["name"], message['tool_calls'][0]['function']['arguments']) #debug
                prompt += f"{role}: {content}\n"
            prompt += "Assistant:\n"
            response = completion_request(self.openai_key, self.base_url, prompt,
                                          model=self.model, process_id=process_id, **args)
            # import pdb; pdb.set_trace()

            try:
                total_tokens = response['usage']['total_tokens']
                message = response["choices"][0]["text"]
                if process_id == 0:
                    print(f"[process({process_id})]total tokens: {total_tokens}")

                if total_tokens >= 8192:
                    message = {
                        "role": "assistant",
                        "content": "The response is too long, please try again.\nOrignal response: " + message,
                        "tool_calls": [
                        {
                            "id": 0,  
                            "function": {
                                "name": 'Finish',
                                "arguments": json.dumps({'return_type': 'give_up_and_restart'}) 
                            },
                            "type": "function"
                        }
                    ]
                    }
                    return message, 0, total_tokens

                thought, action, action_input = react_parser(message)
                # print(message)
                # import pdb; pdb.set_trace()
                random_id = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
                message = {
                    "role": "assistant",
                    "content": message,
                    "tool_calls": [
                        {
                            "id": random_id,  # 可能在conver_to_answer_format处有bug
                            "function": {
                                "name": action,
                                "arguments": action_input 
                            },
                            "type": "function"
                        }
                    ]
                }
                # breakpoint()
                return message, 0, total_tokens
            except BaseException as e:
                print(f"[process({process_id})]Parsing Exception: {repr(e)}. Try again.")
                traceback.print_exc()
                if response is not None:
                    print(f"[process({process_id})]OpenAI return: {response}")
            

        return {"role": "assistant", "content": str(response)}, -1, 0


if __name__ == "__main__":
    llm = ToolLLaMA_vllm(
        model="ToolBench/ToolLLaMA-2-7b-v2",
        openai_key="EMPTY", 
        base_url=""
    )
    messages = [
        {'role': 'system', 'content': 'You are AutoGPT, you can use many tools(functions) to do the following task.\nFirst I will give you the task description, and your task start.\nAt each step, you need to give your thought to analyze the status now and what to do next, with a function call to actually excute your step.\nAfter the call, you will get the call result, and you are now in a new state.\nThen you will analyze your status now, then decide what to do next...\nAfter many (Thought-call) pairs, you finally perform the task, then you can give your finial answer.\nRemember: \n1.the state change is irreversible, you can\'t go back to one of the former state, if you want to restart the task, say "I give up and restart".\n2.All the thought is short, at most in 5 sentence.\n3.You can do more then one trys, so if your plan is to continusly try some conditions, you can do one of the conditions per try.\nLet\'s Begin!\nTask description: You should use functions to help handle the real time user querys. Remember:\n1.ALWAYS call "Finish" function at the end of the task. And the final answer should contain enough information to show to the user,If you can\'t handle the task, or you find that function calls always fail(the function is not valid now), use function Finish->give_up_and_restart.\n2.Do not use origin tool names, use only subfunctions\' names.\nYou have access of the following tools:\n1.viewdns: Your one source for DNS related tools! dns, info, reverse ip, pagerank, portscan, port scan, lookup, records, whois, ipwhois, dnstools, web hosting, hosting, traceroute, dns report, dnsreport, ip location, ip location finder, spam, spam database, dnsbl, propagation, dns propagation checker, checker, china, chinese, firewall, great firewall, is my site down, is site down, site down, down, dns propagate\n'}, 
        {'role': 'user', 'content': "\nWhat's the weather like in San Francisco, Tokyo, and Paris?\nBegin!\n"}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    llm.change_messages(messages)
    output, error_code, token_usage = llm.parse(tools=tools, process_id=0)
    print(output)
    print(token_usage)
