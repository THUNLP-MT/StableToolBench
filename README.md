<div align= "center">
    <h1> StableToolBench</h1>
</div>

<div align="center">

</div>

<p align="center">
  <a href="">Project</a> •
  <a href="#server">Server</a> •
  <a href="#solvable_queries">Solvable Queries</a> •
  <a href="#stable-eval">Stable ToolEval</a> •
  <a href="">Paper</a> •
  <a href="#citation">Citation</a>

</p>

</div>

🔨Welcome to StableToolBench. Faced with the instability of Tool Learning benchmarks, especially ToolBench (Qin et al., 2023), we developed this new benchmark aiming to balance the stability and reality.

## Features
- **Virtual API System**, which comprises a caching system and API simulators. The caching system stores API call responses to ensure consistency, while the API simulators, powered by LLMs, are used for unavailable APIs.
- **A New Set of Solvable Queries**. Query solvability is hard to determine on the fly, causing sigificant randomness and instability. In StableToolBench, we use state-of-the-art LLMs to determine task solvability to filter queries beforehand. 
- **Stable Evaluation System**: Implements a two-phase evaluation process using GPT-4 as an automatic evaluator. It involves judging the solvability of tasks and employing metrics like Solvable Pass Rate (SoPR) and Solvable Win Rate (SoWR).


### Next Steps

## The Virtual API Server
Our virtual API server featured two components, the API simulation system with GPT 4 Turbo and the caching system. We provided three ways to use the virtual API system: the public server for directly calling, a docker container, and the source code.

### The Public Server

### The Docker Container


### Building from Source
To start the server, you need to provide a cache directory and an OpenAI key.

#### Downloading the cache
We provide a cache to download from [Google Drive](). After downloading the cache, unzip the folder into the `server` folder and ensure the `server` folder contains `tool_response_cache` folder and `tools` folder. The resulting folder of `server` looks like:
```
├── /server/
│  ├── /tools/
│  │  └── ...
│  ├── /tool_response_cache/
│  │  └── ...
│  ├── config.yml
│  ├── main.py
│  ├── utils.py
```

#### Running the server
You need to first specify your configurations in `server/config.yml` before running the server. Parameters needed are:
 - `api_key`: The API key for OpenAI models.
 - `api_base`: The API base for OpenAI models if you are using Azure.
 - `model`: The OpenAI model to use. The default value is gpt-4-turbo-preview.
 - `temperature`: The temperature for LLM simulation. The default value is 0.
 - `toolbench_url`: The real ToolBench server URL. The default value is `http://8.218.239.54:8080/rapidapi`.
 - `tools_folder`: The tools enviroment folder path. Default to `./tools`.
 - `cache_folder`: The cache folder path. Default to `./tool_response_cache`.
 - `is_save`: A flag to indicate whether to save real and simulated response into the cache. The new cache is saved at `./tool_response_new_cache`.
 - `port`: The server port to run on, default to 8080.

Now you can run the server by running:
```
cd server
python main.py
```
The server will be run at `http://0.0.0.0:{port}/virtual`. 
To use the server, you will further need a toolbench key. You can apply one from this [form](https://forms.gle/oCHHc8DQzhGfiT9r6).

You can test the server with
```
import requests
import json
import os

url = 'http://0.0.0.0:8080/virtual'
data = {
    "category": "Media",
    "tool_name": "newapi_for_media",
    "api_name": "url",
    "tool_input": {'url': 'https://api.socialmedia.com/friend/photos'},
    "strip": "",
    "toolbench_key": ""
}
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.text)
```



## Inference With Our StableToolBench Server
We currently implemented all models and algorithms supported by ToolBench. We show ChatGPT (`gpt-3.5-turbo-16k`) with CoT as an example here. The script is also shown in `inference_chatgpt_pipeline_virtual.sh`

To use ChatGPT, run:
```bash
export TOOLBENCH_KEY=""
export OPENAI_KEY=""
export PYTHONPATH=./
python toolbench/inference/qa_pipeline.py \
    --tool_root_dir data/toolenv/tools/ \
    --backbone_model chatgpt_function \
    --openai_key $OPENAI_KEY \
    --max_observation_length 1024 \
    --method DFS_woFilter_w2 \
    --input_query_file data/test_instruction/G1_instruction.json \
    --output_answer_file chatgpt_dfs_inference_result \
    --toolbench_key $TOOLBENCH_KEY
```


## StableToolEval


#### Evaluation
*If you want to reproduce the official results, download the reproduction data `reproduction_data.zip` through [Google Drive](https://drive.google.com/drive/folders/1yBUQ732mPu-KclJnuQELEhtKakdXFc3J), unzip it and put the `reproduction_data` under `ToolBench/data/`, and skip the data preparation process.*
- Data preparation. To evaluate your own model and method using ToolEval, first you need to prepare all the model predictions for the six test subsets. Create a directory naming with your model and method, e.g. `chatgpt_cot` then put each test set's predictions under the directory. The file sturcture of the directory should be:
```
├── /chatgpt_cot/
│  ├── /G1_instruction/
│  │  ├── /10160_CoT@1.json
│  │  └── ...
│  ├── /G1_tool/
│  │  ├── /10221_CoT@1.json
│  │  └── ...
│  ├── ...
│  ├── /G3_instruction/
│  │  ├── /10221_CoT@1.json
│  │  └── ...
```

Then preprocess the predictions by running the following commands:
```bash
export RAW_ANSWER_PATH=../../data/reproduction_data/model_predictions/
export CONVERTED_ANSWER_PATH=../../data/reproduction_data/model_predictions_converted/
export MODEL_NAME=chatgpt_cot
export METHOD=CoT
mkdir ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
for test_set in G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
do
    answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
    output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
    python convert_to_answer_format.py\
        --answer_dir ${answer_dir} \
        --method ${METHOD} \
        --output ${output_file}
done
```
After that, check if there are preprocessed json files for the test sets under `${CONVERTED_ANSWER_PATH}/${MODEL_NAME}`. If so, you're ready to run the following evaluate process. If not, check if there is anything wrong with the model's predictions.

- OpenAI Key. Prepare your openai key to use our evaluator. The key(s) should be stored in a json file, e.g. `path/to/your/openai_key_json_file.json`:
```bash
[
    {
        "username": "your_user_name",
        "passwd": "your_password",
        "api_key": "your_openai_key",
        "organization": "your_organization"
    },
    ...
]
```

- Pass rate:
```bash
export CONVERTED_ANSWER_PATH=../../data/reproduction_data/model_predictions_converted/
export SAVE_PATH=pass_rate_results
export CANDIDATE_MODEL=chatgpt_cot
export API_POOL_FILE=path/to/your/openai_key_json_file.json

python eval_pass_rate.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --save_path ${SAVE_PATH} \
    --reference_model ${CANDIDATE_MODEL} \
    --test_ids ../../data/test_ids/ \
    --max_eval_threads 20 \
    --evaluate_times 7

```
The result files will be stored under the ${SAVE_PATH}.

- Win rate. The below example take ChatGPT-ReACT as reference model and GPT4-ReACT as candidate model. Notice that you need to get both model's pass rate results first, then run the following commands to evaluate the preference result of GPT4-ReACT:
```bash
export CONVERTED_ANSWER_PATH=../../data/reproduction_data/model_predictions_converted/
export SAVE_PATH=preference_results
export PASS_TARE_PATH=pass_rate_results
export REFERENCE_MODEL=chatgpt_cot
export CANDIDATE_MODEL=gpt-4-0613_cot
export API_POOL_FILE=path/to/your/openai_key_json_file.json

python eval_preference.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --reference_model ${REFERENCE_MODEL} \
    --output_model ${CANDIDATE_MODEL} \
    --test_ids ../../data/test_ids/ \
    --save_path ${SAVE_PATH} \
    --pass_rate_result_path ${PASS_TARE_PATH} \
    --max_eval_threads 20 \
    --use_pass_rate true \
    --evaluate_times 7
```
The result files will be stored under the ${SAVE_PATH}.

Please refer to [ToolEval](https://github.com/OpenBMB/ToolBench/tree/master/toolbench/tooleval) for more details.

### 📊 Model Experiments Results


In our main experiments, ToolLLaMA(v2) demonstrates a compelling capability to handle both single-tool and complex multi-tool instructions, which on a par with ChatGPT.
Below are the main results. Win rate for each model is compared with ChatGPT-ReACT.


**Pass Rate:**
| Method | Model               | I1-Inst. | I1-Tool | I1-Cate. | I2-Inst. | I2-Cate. | I3-Inst. | Average |
|--------|---------------------|----------|---------|----------|----------|----------|----------|---------|
| ReACT  | Claude-2            | 5.5      | 3.5     | 5.5      | 6        | 6        | 14       | 6.8     |
|        | Text-Davinci-003    | 12       | 20      | 20       | 8.5      | 14.5     | 24       | 16.5    |
|        | ChatGPT             | 41.5     | 44      | 44.5     | 42.5     | 46.5     | 22       | 40.2    |
|        | ToolLLaMA           | 25       | 29      | 33       | 30.5     | 31.5     | 25       | 29      |
|        | GPT4                | 53.5       | 50.0    | 53.5       | 67.0     | 72.0     | 47.0       | 57.2    |
| DFSDT  | Claude-2            | 20.5     | 31      | 18.5     | 17       | 20.5     | 28       | 22.6    |
|        | Text-Davinci-003    | 43.5     | 44      | 46       | 37       | 42       | 46       | 43.1    |
|        | ChatGPT             | 54.5     | 65      | 60.5     | 75       | 71.5     | 62       | 64.8    |
|        | ToolLLaMA           | 57       | 61      | 62       | 77       | 77       | 66       | 66.7    |
|        | ToolLLaMA-Retreiver | **64**       | 64      | 60.5     | **81.5**     | 68.5     | 65       | 67.3    |
|        | GPT4                | 60       | **71.5**    | **67**       | 79.5     | **77.5**     | **71**       | **71.1**    |


**Win Rate:** (Reference model: ChatGPT-ReACT)
| Method | Model               | I1-Inst. | I1-Tool | I1-Cate. | I2-Inst. | I2-Cate. | I3-Inst. | Average |
|--------|---------------------|----------|---------|----------|----------|----------|----------|---------|
| ReACT  | Claude-2            | 31       | 27.8    | 33.8     | 35       | 31.5     | 47.5     | 34.4    |
|        | Text-Davinci-003    | 28.5     | 35.3    | 31       | 29.8     | 29.8     | 45       | 33.2    |
|        | ToolLLaMA           | 45       | 42      | 47.5     | 50.8     | 41.8     | 55       | 47      |
|        | GPT4                | 60       | 58.8    | 63.5     | 65.8     | 60.3     | 78       | 64.4    |
| DFSDT  | Claude-2            | 38       | 44.3    | 43.3     | 36.8     | 33.5     | 65       | 43.5    |
|        | Text-Davinci-003    | 40.3     | 43.8    | 46.8     | 40.5     | 43.3     | 63       | 46.3    |
|        | ChatGPT             | 60.5     | 62      | 57.3     | 72       | **64.8**     | 69       | 64.3    |
|        | ToolLLaMA           | 55       | 55.3    | 54.5     | 68.5     | 58       | 69       | 60      |
|        | ToolLLaMA-Retreiver | 62.3     | 59      | 55       | 68.5     | 60.8     | 73       | 63.1    |
|        | GPT4                | **67.5**     | **67.8**    | **66.5**     | **73.3**     | 63.3     | **84**       | **70.4**    |

## Citation
Feel free to cite us if you like StableToolBench.

```