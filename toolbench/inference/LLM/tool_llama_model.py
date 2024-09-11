#!/usr/bin/env python
# coding=utf-8
import time
from termcolor import colored
from typing import Optional, List
import torch
from typing import Optional
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)
from toolbench.utils import process_system_message
from toolbench.model.model_adapter import get_conversation_template
from toolbench.inference.utils import SimpleChatIO, generate_stream, react_parser
import json, string, random


class ToolLLaMA:
    def __init__(
            self, 
            model_name_or_path: str, 
            template:str="tool-llama-single-round", 
            device: str="cuda", 
            cpu_offloading: bool=False, 
            max_sequence_length: int=8192
        ) -> None:
        super().__init__()
        self.model_name = model_name_or_path
        self.template = template
        self.max_sequence_length = max_sequence_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=False, model_max_length=self.max_sequence_length)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path, low_cpu_mem_usage=True, device_map='auto'
        )
        if self.tokenizer.pad_token_id == None:
            self.tokenizer.add_special_tokens({"bos_token": "<s>", "eos_token": "</s>", "pad_token": "<pad>"})
            self.model.resize_token_embeddings(len(self.tokenizer))
        self.use_gpu = (True if device.startswith("cuda") else False)
        # if (device == "cuda" and not cpu_offloading) or device == "mps":
        #     self.model.to(device)
        self.chatio = SimpleChatIO()

    def prediction(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        with torch.no_grad():
            gen_params = {
                "model": "",
                "prompt": prompt,
                "temperature": 0,
                "max_new_tokens": 1024,
                "stop": "</s>",
                "stop_token_ids": None,
                "echo": False
            }
            generate_stream_func = generate_stream
            output_stream = generate_stream_func(self.model, self.tokenizer, gen_params, "cuda", self.max_sequence_length, force_generate=True)
            outputs = self.chatio.return_output(output_stream)
            prediction = outputs.strip()
        return prediction
        
    def add_message(self, message):
        self.conversation_history.append(message)

    def change_messages(self,messages):
        self.conversation_history = messages

    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        print("before_print"+"*"*50)
        for message in self.conversation_history:
            print_obj = f"{message['role']}: {message['content']} "
            # if "function_call" in message.keys():
            #     print_obj = print_obj + f"function_call: {message['function_call']}"
            if "function_call" in message.keys():
                print_obj = print_obj + f"function_call: {message['function_call']}"
            if 'tool_calls' in message.keys():
                print_obj = print_obj + f"tool_calls: {message['tool_calls']}"
                print_obj = print_obj + f"number of tool calls: {len(message['tool_calls'])}"
            if detailed:
                print_obj = print_obj + f"function_call: {message['function_call']}"
                print_obj = print_obj + f"tool_calls: {message['tool_calls']}"
                print_obj = print_obj + f"function_call_id: {message['function_call_id']}"
            print_obj += ""
            print(
                colored(
                    print_obj,
                    role_to_color[message["role"]],
                )
            )
        print("end_print"+"*"*50)

    def parse(self, tools, process_id, **args):
        conv = get_conversation_template(self.template)
        if self.template == "tool-llama":
            roles = {"human": conv.roles[0], "gpt": conv.roles[1]}
        elif self.template == "tool-llama-single-round" or self.template == "tool-llama-multi-rounds":
            roles = {"system": conv.roles[0], "user": conv.roles[1], "function": conv.roles[2], "tool": conv.roles[2], "assistant": conv.roles[3]}

        self.time = time.time()
        conversation_history = self.conversation_history

        if tools != []:
            functions = [tool['function'] for tool in tools]


        prompt = ''
        for message in conversation_history:
            role = roles[message['role']]
            content = message['content']
            if role == "System" and tools != []:
                content = process_system_message(content, functions=functions)
            prompt += f"{role}: {content}\n"
        prompt += "Assistant:\n"
        if tools != []:
            predictions = self.prediction(prompt)
        else:
            predictions = self.prediction(prompt)

        decoded_token_len = len(self.tokenizer(predictions))
        if process_id == 0:
            print(f"[process({process_id})]total tokens: {decoded_token_len}")

        # react format prediction
        thought, action, action_input = react_parser(predictions)
        random_id = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
        message = {
            "role": "assistant",
            "content": predictions,
            "tool_calls": [{
                'id': f"call_{random_id}",
                'type': "function",
                'function': {
                    'name': action,
                    'arguments': action_input
                }
            }]
        }
        return message, 0, decoded_token_len


if __name__ == "__main__":
    # can accept all huggingface LlamaModel family

    llm = ToolLLaMA("ToolBench/ToolLLaMA-2-7b-v2", device="cuda")

    messages = [
        {'role': 'system', 'content': '''You are AutoGPT, you can use many tools(functions) to do
the following task.\nFirst I will give you the task description, and your task start.\nAt each step, you need to give your thought to analyze the status now and what to do next, with a function call to actually excute your step.\nAfter the call, you will get the call result, and you are now in a new state.\nThen you will analyze your status now, then decide what to do next...\nAfter many (Thought-call) pairs, you finally perform the task, then you can give your finial answer.\nRemember: \n1.the state change is , you can\'t go
back to the former state, if you want to restart the task, say "I give up and restart".\n2.All the thought is short, at most in 5 sentence.\nLet\'s Begin!\nTask description: Use numbers and basic arithmetic operations (+ - * /) to obtain exactly one number=24. Each
step, you are only allowed to choose two of the left numbers to obtain a new number. For example, you can combine [3,13,9,7] as 7*9 - 3*13 = 24.\nRemember:\n1.all of the number must be used , and must be used ONCE. So Only when left numbers is exact 24, you will win. So you don\'t succeed when left number = [24, 5]. You succeed when left number = [24]. \n2.all the try takes exactly 3 steps, look
at the input format'''},
        {"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}
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

