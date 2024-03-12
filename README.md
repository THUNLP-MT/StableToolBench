<div align= "center">
    <h1> StableToolBench</h1>
</div>

<div align="center">

</div>

<p align="center">
  <!-- <a href="">Project</a> • -->
  <a href="#server">Server</a> •
  <a href="#solvable_queries">Solvable Queries</a> •
  <a href="#stable-eval">StableToolEval</a> •
  <a href="">Paper</a> •
  <!-- <a href="#citation">Citation</a> -->

</p>

</div>

🔨Welcome to **StableToolBench**. Faced with the instability of Tool Learning benchmarks, especially ToolBench (Qin et al., 2023), we developed this new benchmark aiming to balance the stability and reality.

## Features
- **Virtual API System**, which comprises a caching system and API simulators. The caching system stores API call responses to ensure consistency, while the API simulators, powered by LLMs, are used for unavailable APIs.
- **A New Set of Solvable Queries**. Query solvability is hard to determine on the fly, causing sigificant randomness and instability. In StableToolBench, we use state-of-the-art LLMs to determine task solvability to filter queries beforehand. 
- **Stable Evaluation System**: Implements a two-phase evaluation process using GPT-4 as an automatic evaluator. It involves judging the solvability of tasks and employing metrics like Solvable Pass Rate (SoPR) and Solvable Win Rate (SoWR).


## The Virtual API Server {#server}
<!-- Our Virtual API server featured two components, the API simulation system with GPT 4 Turbo and the caching system. We provided three ways to use the virtual API system: the public server for directly calling, a docker container, and the source code. -->
Our Virtual API server featured two components, the API simulation system with GPT 4 Turbo and the caching system. You can pull the source of the codes and download relevant data to run it.
<!-- ### The Public Server

### The Docker Container -->


### Building from Source
Before you run any code, please first setup the environment by running `pip install -r requirements.txt`.

To start the server, you need to provide a cache directory and an OpenAI key.

#### Downloading the cache
We provide a cache to download from [Google Drive](https://drive.google.com/file/d/1XUiCMA5NV359UGR-eknF0TcXORuR7RXj/view?usp=sharing) or [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/07ee752ad20b43ed9b0d/?dl=1). After downloading the cache, unzip the folder into the `server` folder and ensure the `server` folder contains `tool_response_cache` folder and `tools` folder. The resulting folder of `server` looks like:
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
The server will be run at `http://localhost:{port}/virtual`. 
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


## Solvable Queries {#solvable_queries}
The original queries are curated without considering the solvability but judging the solvability with ChatGPT on the fly will cause sigificant instability. Therefore, we judge the solvability of the original queries with majority vote of `gpt-4-turbo`, `gemini-pro` and `claude-2`. The filtered queries are saved in `solvable_queries`.


## Inference With Our StableToolBench Server
If you have not set up the environment, please first do so by running `pip install -r requirements.txt`.
We currently implemented all models and algorithms supported by ToolBench. We show ChatGPT (`gpt-3.5-turbo-16k`) with CoT as an example here. The script is also shown in `inference_chatgpt_pipeline_virtual.sh`. An example of results is shown in `data_example/answer`.

To use ChatGPT, run:
```bash
export TOOLBENCH_KEY=""
export OPENAI_KEY=""
export OPENAI_API_BASE="" 
export PYTHONPATH=./
export GPT_MODEL="gpt-3.5-turbo-16k"
export SERVICE_URL="http://localhost:8080/virtual"
export OUTPUT_DIR="data/answer/virtual_chatgpt_cot"
group=G1_instruction
mkdir -p $OUTPUT_DIR; mkdir -p $OUTPUT_DIR/$group

python toolbench/inference/qa_pipeline_multithread.py \
    --tool_root_dir toolenv/tools \
    --backbone_model chatgpt_function \
    --openai_key $OPENAI_KEY \
    --max_observation_length 1024 \
    --method CoT@1 \
    --input_query_file solvable_queries/test_instruction/${group}.json \
    --output_answer_file $OUTPUT_DIR/$group \
    --toolbench_key $TOOLBENCH_KEY \
    --num_thread 1
```


## StableToolEval {#stable-eval}
We basically follow the evaluation process of ToolBench. The difference is that we update the evaluation logic of Pass Rate and Win Rate, resulting in Solvable Pass Rate and Solvable Win Rate.


The first step is prepare data. This step is the same as ToolEval in ToolBench.
The following paragraph is adapted from ToolBench.
To evaluate your own model and method using ToolEval, first you need to prepare all the model predictions for the six test subsets. Create a directory naming with your model and method, e.g. `chatgpt_cot` then put each test set's predictions under the directory. The file sturcture of the directory should be:
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
cd toolbench/tooleval
export RAW_ANSWER_PATH=../../data_example/answer
export CONVERTED_ANSWER_PATH=../../data_example/model_predictions_converted
export MODEL_NAME=virtual_chatgpt_cot
export test_set=G1_instruction

mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json

python convert_to_answer_format.py\
    --answer_dir ${answer_dir} \
    --method CoT@1 # DFS_woFilter_w2 for DFS \
    --output ${output_file}
```


Next you can calculate the Solvable Pass Rate. Before running the process, you need to specify your evaluation OpenAI key in `openai_key.json` as follows:
```bash
[
    {
        "api_key": "your_openai_key",
        "api_base": "your_organization"
    },
    ...
]
```
Then calculate SoPR with :
```bash
cd  toolbench/tooleval
export API_POOL_FILE=../../openai_key.json
export CONVERTED_ANSWER_PATH=../../data_example/model_predictions_converted
export SAVE_PATH=../../data_example/pass_rate_results
mkdir -p ${SAVE_PATH}
export CANDIDATE_MODEL=virtual_chatgpt_cot
export EVAL_MODEL=gpt-4-turbo-preview
mkdir -p ${SAVE_PATH}/${CANDIDATE_MODEL}

python eval_pass_rate.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --save_path ${SAVE_PATH}/${CANDIDATE_MODEL} \
    --reference_model ${CANDIDATE_MODEL} \
    --test_ids ../../solvable_queries_example/test_query_ids \
    --max_eval_threads 35 \
    --evaluate_times 3 \
    --test_set G1_instruction 

```
Note that we use `gpt-4-turbo-preview` as the standard evaluation model, which provided much better stability than `gpt-3.5` series models.

The result files will be stored under the ${SAVE_PATH}.

Then you can calcualte the SoWR. The below example take ChatGPT-CoT as reference model and ChatGPT-DFS as candidate model. Note that you need to get both model's pass rate results first.
```bash
cd  toolbench/tooleval
export API_POOL_FILE=../../openai_key.json
export CONVERTED_ANSWER_PATH=../../data_example/model_predictions_converted
export SAVE_PATH=../../data_example/preference_results
export PASS_RATE_PATH=../../data_example/pass_rate_results
export REFERENCE_MODEL=virtual_chatgpt_cot
export CANDIDATE_MODEL=virtual_chatgpt_dfs
export EVAL_MODEL=gpt-4-turbo-preview
mkdir -p ${SAVE_PATH}


python eval_preference.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --reference_model ${REFERENCE_MODEL} \
    --output_model ${CANDIDATE_MODEL} \
    --test_ids ../../solvable_queries_example/test_query_ids/ \
    --save_path ${SAVE_PATH} \
    --pass_rate_result_path ${PASS_RATE_PATH} \
    --max_eval_threads 10 \
    --use_pass_rate true \
    --evaluate_times 3 \
    --test_set G1_instruction
```
The result files will be stored under the ${SAVE_PATH}.

### 📊 Model Experiments Results


In our main experiments, ToolLLaMA(v2) demonstrates a compelling capability to handle both single-tool and complex multi-tool instructions, which on a par with ChatGPT.
Below are the main results. Win rate for each model is compared with ChatGPT-ReACT.


**Solvable Pass Rate:**
| **Method** | **I1 Instruction** | **I1 Category** | **I1 Tool** | **I2 Category** | **I2 Instruction** | **I3 Instruction** | **Average** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-3.5-Turbo-0613  (CoT) | 55.9±1.0 | 50.8±0.8 | 55.9±1.0 | 44.1±0.8 | 36.2±0.4 | 51.4±1.5 | 49.1±1.0 |
| GPT-3.5-Turbo-0613 (DFS) | 66.4±1.5 | 64.3±1.0 | 67.2±2.4 | 67.7±0.8 | 61.5±1.0 | 81.4±1.5 | 68.1±1.4 |
| GPT-4-0613 (CoT) | 50.7±0.4 | 57.1±0.3 | 51.9±0.3 | 55.0±1.1 | 61.6±0.8 | 56.3±0.8 | 55.4±0.6 |
| GPT-4-0613 (DFS) | 65.5±1.1 | 62.0±1.7 | 72.1±1.6 | **70.8±1.3** | **73.1±1.4** | 74.9±1.5 | 69.7±1.4 |
| ToolLLaMA v2 (CoT) | 37.2±0.1 | 42.3±0.4 | 43.0±0.5 | 37.4±0.4 | 33.6±1.2 | 39.6±1.0 | 38.9±0.6 |
| ToolLLaMA v2 (DFS) | 59.8±1.5 | 59.5±1.4 | 65.7±1.1 | 56.5±0.3 | 47.6±0.4 | 62.8±1.9 | 58.7±1.1 |
| GPT-3.5-Turbo-1106 (CoT) | 51.3±0.6 | 48.8±0.3 | 59.9±0.8 | 50.8±0.7 | 43.2±0.8 | 58.5±0.8 | 52.1±0.7 |
| GPT-3.5-Turbo-1106 (DFS) | 67.8±0.9 | 67.2±0.3 | **72.9±0.7** | 63.2±1.0 | 70.9±0.4 | 77.6±0.8 | 69.9±0.7 |
| GPT-4-Turbo-Preview (CoT) | 63.1±1.0 | 64.5±0.5 | 55.3±0.3 | 63.0±0.8 | 57.3±0.8 | 61.7±0.8 | 60.8±0.7 |
| GPT-4-Turbo-Preview (DFS) | **70.8±1.0** | **71.1±0.7** | 70.4±1.2 | 70.4±1.3 | 71.7±0.4 | **84.7±1.7** | **73.2±1.1** |

In this experiment, we run all models once, evaluate three times and take the average results. C and D stand for CoT and DFS respectively. The experiments below follow the denotation.


**Solvable Win Rate:** (Reference model: ChatGPT-CoT)
| **Method** | **I1 Instruction** | **I1 Category** | **I1 Tool** | **I2 Category** | **I2 Instruction** | **I3 Instruction** | **Average** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-3.5-Turbo-0613 (DFS) | 57.7 | 60.8 | 61.4 | 66.1 | 63.2 | 70.5 | 63.3 |
| GPT-4-0613 (CoT) | 50.3 | 54.2 | 50.6 | 50.0 | 64.2 | 55.7 | 54.2 |
| GPT-4-0613 (DFS) | 57.1 | 60.1 | 57.0 | 64.5 | 74.5 | 72.1 | 64.2 |
| ToolLLaMA v2 (CoT) | 35.0 | 30.7 | 37.3 | 31.5 | 36.8 | 23.0 | 32.4 |
| ToolLLaMA v2 (DFS) | 43.6 | 45.1 | 38.6 | 42.7 | 53.8 | 45.9 | 44.9 |
| GPT-3.5-Turbo-1106 (CoT) | 46.6 | 45.1 | 48.1 | 44.4 | 37.7 | 52.5 | 45.7 |
| GPT-3.5-Turbo-1106 (DFS) | 56.4 | 54.2 | 51.9 | 54.0 | 62.3 | 72.1 | 58.5 |
| GPT-4-Turbo-Preview (CoT) | 68.7 | 71.9 | 58.2 | 71.0 | 76.4 | 73.8 | 70.0 |
| GPT-4-Turbo-Preview (DFS) | **66.9** | **73.9** | **68.4** | **72.6** | **78.3** | **77.0** | **72.9** |

Table: Solvable Win Rate scores. We run all models once against `GPT-3.5-Turbo-0613 + CoT` and evaluate three times. We follow the ToolBench implementation to take the most frequent result for each query during evaluation.

<!-- ## Citation
Feel free to cite us if you like StableToolBench.

``` -->