import os, sys
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.requests import Request
import uvicorn
import time
import json
import yaml
import requests
from typing import Union
from utils import standardize, change_name

from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import openai
import re


config_file='config_mirrorapi_cache.yml'
CONFIG = yaml.load(open(config_file, 'r'), Loader=yaml.FullLoader)
print(CONFIG)

from openai import OpenAI, AzureOpenAI
if 'api_base' in CONFIG:
    OPENAI_API_BASE=CONFIG['api_base']
else:
    OPENAI_API_BASE="https://api.openai.com/v1"
OPENAI_API_KEY=CONFIG['api_key']


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class Info(BaseModel):
    category: str
    tool_name: str
    api_name: str
    tool_input: Union[str, dict]
    strip: str
    toolbench_key: str

def prepare_tool_name_and_url(info):
    category = info.category
    standard_category = category.replace(" ", "_").replace(",", "_").replace("/", "_")
    while " " in standard_category or "," in standard_category:
        standard_category = standard_category.replace(" ", "_").replace(",", "_")
    standard_category = standard_category.replace("__", "_")
    
    tool_name = info.tool_name
    api_name = change_name(standardize(info.api_name)).split(f"_for_{tool_name}")[0]
    if not tool_name.endswith(f"_for_{standard_category}"):
        tool_name = standardize(info.tool_name)
        code_string = f"""from my_tools.{standard_category}.{tool_name}.api import {api_name}"""
        tool_name += f"_for_{standard_category}"
    else:
        tmp_tool_name = standardize(tool_name.replace(f"_for_{standard_category}", ""))
        code_string = f"""from my_tools.{standard_category}.{tmp_tool_name}.api import {api_name}"""
    return tool_name, standard_category, api_name, code_string

@app.post('/virtual')
# @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(1))
def get_virtual_response(request: Request, info: Info):
    user_key = info.toolbench_key

    print(info)
    print(request)
    
    tool_name, standard_category, api_name, code_string = prepare_tool_name_and_url(info)
    tool_input = info.tool_input
    tool_name_original = info.tool_name

    if api_name == "chat_with_user":
        return {"error": "", "response": "Chat with user."}
    
    try:
        tool_input = json.loads(tool_input)
    except Exception as e:
        if tool_input == "":
            tool_input = {}
        elif isinstance(tool_input, dict):
            tool_input = tool_input
        else:
            print(f"Can not parse tool input into json: {tool_input}")
            print(type(tool_input))
            print(tool_input)
            response_dict = {"error": f"Tool input parse error...\n", "response": ""}
            return response_dict



    
    if "_for_" in tool_name_original:
        tool_name_real = tool_name_original.split("_for_")[0]
    else:
        tool_name_real = tool_name_original
    data = {
        "category": standard_category,
        "tool_name": tool_name_real,
        "api_name": api_name,
        "tool_input": tool_input,
        "strip": "",
        "toolbench_key": user_key
    }
    


    """
    Fake response function here. 
    result = fake_response_function(api_doc, api_name, api_parameters, *kwargs)
    """

    # parse api_doc
    tool_name_original = standardize(tool_name_original)
    api_name = standardize(api_name)
    api_doc = {
        'tool_description': "",
        'api_info': "",
    }
    try:
        if os.path.exists(os.path.join(CONFIG['tools_folder'], standard_category)):
            if os.path.exists(os.path.join(CONFIG['tools_folder'], standard_category, tool_name_original.split("_for_")[0]+".json")):
                # read json
                api_intro = json.load(open(os.path.join(CONFIG['tools_folder'], standard_category, tool_name_original.split("_for_")[0]+".json"), "r"))
                # get tool_dexcription and api_info
                tool_description = api_intro['tool_description']
                api_info = []
                for api in api_intro['api_list']:
                    if api_name == standardize(api['name']):
                        api_info.append(api)
                # check invalid api name
                if len(api_info) == 0:
                    print("cant match api name")
                api_doc = {
                    'tool_description': tool_description,
                    'api_info': api_info
                }
            else:
                print(f"cant get {tool_name_original}")
    except Exception as e:
        print(f"Loading api_doc error: {e}")


        
    result = fake_response_function_with_trained_simulator(tool_input, data, api_doc, api_name)
    print(f"fake result: {result}")


    if not isinstance(result, dict):
        return json.loads(result)
    else:
        return result
    
def is_valid_json(result):
    """
    Checks if the given string is valid JSON.

    Args:
      data: The string to be checked.

    Returns:
      True if the string is valid JSON, False otherwise.
    """
    # check json format
    try:
        result = json.loads(result)
        return True
    except Exception as e:
        print(f"Can not parse result into json: {result}")
        return False

def extract_attributes_json(output):
    # Extract the values
    try:
        output_dict = json.loads(output)
    except:
        # Regular expression to capture "error" and "response" fields
        if "mechanism_of_the_api" in output:
            pattern = (
                r'"mechanism_of_the_api"\s*:\s*"(.*?)",\s*'   # Capture mechanism_of_the_api
                r'"error"\s*:\s*"(.*?)",\s*'                 # Capture error
                r'"response"\s*:\s*"(.*)'                    # Capture response (no final quote)
            )
            match = re.search(pattern, output, re.DOTALL)

            if match:
                reason_content = match.group(1)
                error_content = match.group(2)  # Extract error content
                response_content = match.group(3)  # Extract response content
                output_dict = {"error": error_content, "response": response_content}
            else:
                print("No matches found.")
                return None, None, None
        else:
            pattern = r'"error":\s*"([^"]*)",\s*"response":\s*"(.*)'
        # Search for matches
            match = re.search(pattern, output, re.DOTALL)

            if match:
                error_content = match.group(1)  # Extract error content
                response_content = match.group(2)  # Extract response content
                output_dict = {"error": error_content, "response": response_content}
            else:
                print("No matches found.")
                return None, None, None
    error, response = output_dict['error'], output_dict['response']
    return None, error, response


def check_result(processes_value: dict):
    if 'error' not in processes_value or processes_value['error'] != '':
        return False
    if 'response' not in processes_value:
        return False
    response = str(processes_value['response'])
    if 'got an unexpected keyword argument' in response.lower():
        return True
    elif 'rate limit' in response.lower() or 'time out' in response.lower() or 'timed out' in response.lower() or 'does not exist' in response.lower() or '404' in response.lower() or '504' in response.lower() or '500' in response.lower() or 'internal error' in response.lower() or 'API doesn\'t exists' in response.lower() or "API doesn\'t exists" in response.lower() or response == '{\'message\': "API doesn\'t exists"}' or 'Service Not Found' in response:
        return False
    elif 'authoriz' in response.lower() or 'authenticat' in response.lower() or 'unauthorized' in response.lower() or 'blocked user' in response.lower() or 'unsubscribe' in response.lower() or 'blocked' in response.lower() or '401' in response.lower() or '403' in response.lower() or 'credential' in response.lower() or 'unauthenticated' in response.lower() or 'disabled for your subscription' in response.lower() or 'ACCESS_DENIED' in response:
        return False
    elif 'parameter' in response.lower() or 'parse' in response.lower() or 'is not defined' in response.lower():
        return False
    elif len(response) == 0:
        return False
    elif "status_code=50" in response or "status_code=429" in response:
        return False
    return True


def fake_response_function_with_trained_simulator(tool_input, data, api_doc, api_name):
    '''
    api_example: list of tuple, [(input, output), ...]
    tool_input: dict, input of the tool
    api_doc: dict, api document
    '''
    from system_prompts import SFT_SYSTEM

    USER_PROMPT = """\
API doc:
{api_doc}

Request:
{request}\
"""

    api_doc = {
        "api_name": api_name,
        "api_description": api_doc['api_info'][0]['description'],
        "required_parameters": api_doc['api_info'][0]['required_parameters'],
        "optional_parameters": api_doc['api_info'][0]['optional_parameters'],
        "tool_description": api_doc['tool_description'],
        "tool_name": data['tool_name'],
        "tool_category": data['category'],
    }
    print(f"api_doc: {api_doc}")
    request = {**tool_input}
    if 'toolbench_key' in request:
        request.pop('toolbench_key')
    instruction = USER_PROMPT.format(api_doc=api_doc, request=request)
    print(instruction)
    messages = [
        {"role": "system", "content": SFT_SYSTEM},
        {"role": "user", "content": instruction},
    ]

    client = openai.OpenAI(
        base_url=OPENAI_API_BASE,
        api_key=OPENAI_API_KEY,
    )
    generate_text = client.chat.completions.create(
        model=CONFIG.get('model', 'simulation-250123-qwen25-mixed'),
        messages=messages,
        temperature=CONFIG['temperature'],
        max_tokens=2048,
        seed=42
    )
    generate_text = generate_text.choices[0].message.content


    model = CONFIG.get('model', 'simulation-250123-qwen25-mixed')
    model = model.split("/")[-1]
    
    _, error, response = extract_attributes_json(generate_text)
    if error or response:
        return json.dumps({"error": error, "response": response})
    else:
        fake_error = {
            "error": "Failed to generate fake response",
            "response": "",
        }
        return json.dumps(fake_error)





if __name__ == "__main__":
    uvicorn.run(app="main_mirrorapi_cache:app", host="0.0.0.0", port=CONFIG['port'])

