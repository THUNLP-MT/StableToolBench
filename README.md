<div align= "center">
    <h1> <img src="stbicon.svg" alt="favicon" style="width: 35px; height: auto;"> StableToolBench</h1>
</div>

<div align="center">

</div>

<p align="center">
  <a href="https://zhichengg.github.io/stb.github.io/">Project</a> •
  <a href="#the-virtual-api-server">Server</a> •
  <a href="#solvable-queries">Solvable Queries</a> •
  <a href="#inference-with-our-stabletoolbench-server">Inference</a> •
  <a href="#stabletooleval">StableToolEval</a> •
  <a href="https://arxiv.org/pdf/2403.07714.pdf">Paper</a> •
  <a href="#citation">Citation</a>

</p>


Welcome to **StableToolBench**. Faced with the instability of Tool Learning benchmarks, we developed this new benchmark aiming to balance the stability and reality, based on [ToolBench](https://github.com/OpenBMB/ToolBench) (Qin et al., 2023).

## Note for Applying ToolBench keys
Note that if you have applied a ToolBench key but did not get a response for a long time, please contact Shihao Liang (shihaoliang0828@gmail.com) for further assistance.

## Updates from StableToolBench-MirrorAPI
* The new API simulation model, named `MirrorAPI`, which is trained to simulate more than 7k tools in ToolBench. You can download it from [huggingface](https://huggingface.co/stabletoolbench/MirrorAPI).
* The new FAC evaluation for StableToolBench, which takes final answers only into account.

## Updates
- **[2024.09.15]** We found there exist some problems in the inference codes of ToolLLaMA v2 and we update model performance accordingly.
- **[2024.06.19]** We update the OpenAI API to the newest version, which also support parallel function calling now. We also updated the model performance evaluation using `gpt-4-turbo-2024-04-09`, replacing `gpt-4-turbo-preview`, which we found may produce unstable evaluations. The inference results (run in Feb 2024) can be found on [Huggingface](https://huggingface.co/datasets/stabletoolbench/baselines).


## Features
Based on the large scale of ToolBench, we introduce the following features to ensure the stability and reality of the benchmark:
- **MirrorAPI**, which is a trained on real request-response pairs to stably mirror more than 7k API's behaviours.
- **Virtual API System**, which comprises a caching system and API simulators. The caching system stores API call responses to ensure consistency, while the API simulators, powered by LLMs, are used for unavailable APIs. Note that we keep the large-scale diverse APIs environment from ToolBench.
- **A New Set of Solvable Queries**. Query solvability is hard to determine on the fly, causing significant randomness and instability. In StableToolBench, we use state-of-the-art LLMs to determine task solvability to filter queries beforehand. We maintain the same query and answer format as ToolBench for seamless transition from it.
- **Stable Evaluation System**: Implements a two-phase evaluation process using GPT-4 as an automatic evaluator. It involves judging the solvability of tasks and employing metrics like Solvable Pass Rate (SoPR) and Solvable Win Rate (SoWR). Starting with **MirrorAPI**, we also provide an end-to-end trained evaluator, which takes only input query and final answer into account and gives more stable and straightforward evaluation.

## The Virtual API Server
<!-- Our Virtual API server featured two components, the API simulation system with GPT 4 Turbo and the caching system. We provided three ways to use the virtual API system: the public server for directly calling, a docker container, and the source code. -->
We now provide two simulating systems, the MirrorAPI server and the GPT based caching system.

Before you run any code, please first set up the environment by running `pip install -r requirements.txt`.

### The MirrorAPI server

#### Downloading Tools and Models
You need to download a set of tools to start the server. You can use either the tool set we crawled on Apr 2024, which you can download from [HuggingFace](https://huggingface.co/datasets/stabletoolbench/ToolEnv2404) or the tools for the ToolBench/StableToolBench test set, which you can download from [ToolBench](https://github.com/OpenBMB/ToolBench).

We provide two versions of model, the [`MirrorAPI`](https://huggingface.co/stabletoolbench/MirrorAPI),  trained for general tool responses, and [`MirrorAPI-Cache`](https://huggingface.co/stabletoolbench/MirrorAPI-Cache), which is trained on the cache of StableToolBench for better test set tool responses. You can download them from the link above.


#### Starting the server
To start the server, you need to install [`vllm`](https://github.com/vllm-project/vllm). Then you can start a model by running 
```
vllm serve {model-path} --api-key EMPTY --port 12345 --served-model-name {model-name}
``` 
Then you need to fill the model-name, api-key and port you specified in server/config_mirrorapi.yml (or server/config_mirrorapi_cache.yml if you are running `MirrorAPI-Cache`), along with the tool folder you downloaded tools into. The parameters in the config files are:
 - `api_key`: The API key for VLLM model.
 - `api_base`: The API base for VLLM models. Normally `http://127.0.0.1:{port}/v1`
 - `model`: The {model-name} you specified in VLLM.
 - `temperature`: The temperature for LLM simulation. The default value is 0.
 - `tools_folder`: The tools environment folder path. Default to `./tools`.
 - `port`: The server port to run on, default to 8080. 

Then you can run `python main_mirrorapi.py` or `python main_mirrorapi_cache.py` to run the API server.


### The GPT based caching system

Our Virtual API server featured two components, the API simulation system with GPT 4 Turbo and the caching system. We provide two methods to use the virtual API system: [building from source](#building-from-source) and using [our prebuilt Docker](#using-the-prebuilt-docker-image).
<!-- ### The Public Server -->

To start the server, you need to provide a cache directory and an OpenAI key.

#### Downloading the cache
We provide a cache to download from [HuggingFace](https://huggingface.co/datasets/stabletoolbench/Cache) or [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/07ee752ad20b43ed9b0d/?dl=1). After downloading the cache, unzip the folder into the `server` folder and ensure the `server` folder contains `tool_response_cache` folder and `tools` folder. The resulting folder of `server` looks like:
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

#### Running the server directly
You need to first specify your configurations in `server/config.yml` before running the server. Parameters needed are:
 - `api_key`: The API key for OpenAI models.
 - `api_base`: The API base for OpenAI models if you are using Azure.
 - `model`: The OpenAI model to use. The default value is gpt-4-turbo-preview.
 - `temperature`: The temperature for LLM simulation. The default value is 0.
 - `toolbench_url`: The real ToolBench server URL. The default value is `http://8.218.239.54:8080/rapidapi`.
 - `tools_folder`: The tools environment folder path. Default to `./tools`.
 - `cache_folder`: The cache folder path. Default to `./tool_response_cache`.
 - `is_save`: A flag to indicate whether to save real and simulated responses into the cache. The new cache is saved at `./tool_response_new_cache`.
 - `port`: The server port to run on, default to 8080.

Now you can run the server by running:
```
cd server
python main.py
```
The server will be run at `http://localhost:{port}/virtual`. 
To use the server, you will further need a toolbench key. You can apply one from this [form](https://forms.gle/oCHHc8DQzhGfiT9r6).  

#### Running the server using Docker

We provide a `Dockerfile` for easy deployment and consistent server environment. This allows you to run the server on various platforms that support Docker.

***Prerequisites:***

* Docker installed: https://docs.docker.com/engine/install/

***Building the Docker Image:***

1. Navigate to your project directory in the terminal.
2. Build the Docker image using the following command:

```bash
docker build -t my-fastapi-server .  # Replace 'my-fastapi-server' with your desired image name
docker run -p {port}:8080 my-fastapi-server  # Replace 'my-fastapi-server' with your image name
```
#### Using the Prebuilt Docker Image
You can also use our prebuilt Docker image from Docker Hub hosted at https://hub.docker.com/repository/docker/zhichengg/stb-docker/general. 
Before running the docker, you will need to install docker and download the cache files as described in [Building from Source](#building-from-source).
Then you can run the server using the following command:
```bash
docker pull zhichengg/stb-docker:latest
docker run -p {port}:8080 -v {tool_response_cache_path}:/app/tool_response_cache -v {tools_path}:/app/tools -e OPENAI_API_KEY= -e OPENAI_API_BASE= zhichengg/stb-docker
```
Remember to fill in the `port`, `tool_response_cache_path`, and `tools_path` with your own values. The `OPENAI_API_KEY` and `OPENAI_API_BASE` are the OpenAI API key and API base if you are using Azure. The server will be run at `http://localhost:{port}/virtual`.


### Testing the Server
You can test the server with
```
import requests
import json
import os

url = 'http://0.0.0.0:8080/virtual'
data = {
    "category": "Artificial_Intelligence_Machine_Learning",
    "tool_name": "TTSKraken",
    "api_name": "List Languages",
    "tool_input": '{}',
    "strip": "truncate",
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


## Solvable Queries
The original queries are curated without considering the solvability but judging the solvability with ChatGPT on the fly will cause significant instability. Therefore, we judge the solvability of the original queries with the majority vote of `gpt-4-turbo`, `gemini-pro` and `claude-2`. The filtered queries are saved in `solvable_queries`.


## Inference With Our StableToolBench Server
If you have not set up the environment, please first do so by running `pip install -r requirements.txt`.
We currently implement all models and algorithms supported by ToolBench. We show ChatGPT (`gpt-3.5-turbo-16k`) with CoT as an example here. The script is also shown in `inference_chatgpt_pipeline_virtual.sh`. An example of the results is shown in `data_example/answer`.

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


## StableToolEval
We follow the evaluation process of ToolBench. The difference is that we update the evaluation logic of the Pass Rate and Win Rate, resulting in the Solvable Pass Rate and Solvable Win Rate.


The first step is to prepare data. This step is the same as ToolEval in ToolBench.
The following paragraph is adapted from ToolBench.
To evaluate your model and method using ToolEval, you first need to prepare all the model predictions for the six test subsets. Create a directory naming with your model and method, e.g. `chatgpt_cot` then put each test set's predictions under the directory. The file structure of the directory should be:
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


Next, you can calculate the Solvable Pass Rate. Before running the process, you need to specify your evaluation OpenAI key in `openai_key.json` as follows:
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

Then you can calculate the SoWR. The below example takes ChatGPT-CoT as the reference model and ChatGPT-DFS as the candidate model. Note that you need to get both model's pass rate results first.
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


## The MirrorAPI Final-Answer-Correctness (FAC) Evaluation

To run the FAC evaluation, you need to use the converted answer stated above. Then you can run the evaluation by running the following code (also shown in run_fac_eval.sh):
```bash
cd  toolbench/tooleval

export MODEL_PATH="Your path to the FAC model"
export CONVERTED_ANSWER_PATH=../../data_example/model_predictions_converted
export SAVE_PATH=../../data_example/fac_results
mkdir -p ${SAVE_PATH}

GROUP="The group name"
CANDIDATE_MODEL="Your candidiate model"
python tool_eval.py \
                    --model_path $MODEL_PATH \
                    --evaluation_path $MODEL_FILE \
                    --output_path $SAVE_PATH/$CANDIDATE_MODEL/$GROUP.csv \
                    --ids ../../solvable_queries_example/test_query_ids/${GROUP}.json
```

## MirrorAPI Training and Evaluation 
We also publish the data and metrics used in the training and evaluation of MirrorAPI. The training and testing data can be found at [huggingface](https://huggingface.co/datasets/stabletoolbench/MirrorAPI). The newly created ToolBench test set used to compare real and simulated data can also be found at [huggingface](https://huggingface.co/datasets/stabletoolbench/real_simulated_compare).

We use [FastChat](https://github.com/lm-sys/FastChat) to perform LLM-as-a-Judge. The prompt we used can be found at Table 12 of our paper.



### Model Experiments Results

#### MirrorAPI-Cache Based System

**Solvable Pass Rate Score**

We evaluate the results with `gpt-4o`.
| Method              | I1 Inst  | I1 Cat  | I1 Tool  | I2 Cat  | I2 Inst  | I3 Inst  | Average  |
|---------------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| ToolLLaMA v2 CoT   | 28.0±1.9     | 30.5±0.8     | 21.5±0.9     | 19.9±1.0     | 22.3±0.4     | 19.1±0.8     | 22.8±0.8     |
| ToolLLaMA v2 DFS   | 28.4±0.9     | 32.5±0.8     | 22.2±1.0     | 22.8±1.5     | 19.2±1.6     | 18.6±1.5     | 22.9±1.4     |
| GPT 4o mini CoT    | 27.8±1.4     | 34.9±0.3     | 34.2±0.5     | 24.5±1.0     | 22.3±2.7     | 20.8±1.5     | 25.9±1.7     |
| GPT 4o mini DFS    | 26.8±1.4     | 36.4±1.6     | 33.1±1.1     | 25.8±1.7     | 25.8±2.7     | 20.2±0.8     | 26.4±1.6     |
| GPT 4o CoT         | **33.3±2.0** | 35.1±0.6     | 33.6±0.8     | 32.5±1.7     | **29.6±1.6** | **27.9±3.5** | **32.0±2.2** |
| GPT 4o DFS        | 32.7±1.9     | **42.3±1.3** | **34.6±1.3** | **32.8±1.5** | 28.3±1.3     | 23.0±1.3     | 30.9±1.7     |

**FAC Score**
| Method             | I1 Inst | I1 Cat | I1 Tool | I2 Cat | I2 Inst | I3 Inst | Average |
|--------------------|---------|---------|---------|---------|---------|---------|---------|
| ToolLLaMA v2 CoT  | 45.4    | 38.6    | 34.2    | 40.3    | 37.7    | 31.1    | 37.9    |
| ToolLLaMA v2 DFS  | **47.9** | 40.5    | 31.0    | 40.3    | 34.0    | 31.1    | 37.5    |
| GPT 4o mini CoT   | 42.3    | 39.9    | 38.0    | 44.4    | 36.8    | **36.1** | 39.6    |
| GPT 4o mini DFS   | 46.0    | 43.8    | 44.3    | 41.1    | 34.9    | 34.4    | 40.8    |
| GPT 4o CoT        | 45.4    | 43.8    | 44.3    | **54.0** | **45.3** | 32.8    | 44.3    |
| GPT 4o DFS        | 46.6    | **53.6** | **44.9** | 50.0    | 42.5    | 34.4    | **45.3** |



#### GPT Based Caching System
Below are the main results (Inference done in Feb 2024). The win rate for each model is compared with ChatGPT-ReACT. We use `gpt-4-turbo-2024-04-09` as the evaluator. Evaluation done in May 2024.

Note that the ToolLLaMA v2 performance is update on 15 Sep 2024 with the new inference codes. Legacy performance can be found [here](legacy_results.md)

**Solvable Pass Rate:**
| **Method** | **I1 Instruction** | **I1 Category** | **I1 Tool** | **I2 Category** | **I2 Instruction** | **I3 Instruction** | **Average** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-3.5-Turbo-0613 (CoT) | 52.2±1.1 | 47.3±0.6 | 53.6±1.3 | 42.5±2.1 | 35.8±2.0 | 48.1±0.8 | 46.6±1.3 |
| GPT-3.5-Turbo-0613 (DFS) | 60.3±1.3 | 66.2±1.2 | 67.1±0.0 | 59.1±0.4 | 51.3±1.2 | 73.8±2.3 | 63.0±1.1 |
| GPT-4-0613 (CoT) | 45.5±0.4 | 57.4±0.3 | 48.8±0.7 | 43.0±0.7 | 46.5±0.9 | 48.1±1.5 | 48.2±0.8 |
| GPT-4-0613 (DFS) | 57.3±0.6 | 57.3±0.3 | 60.9±1.0 | 57.9±1.0 | 51.3±0.8 | 66.4±2.4 | 58.5±1.0 |
| ToolLLaMA v2 (CoT) | 51.8±0.4 | 53.1±0.6 | 46.4±1.2 | 51.6±1.1 | 48.9±0.4 | 37.2±0.8 | 48.2±0.8 |
| ToolLLaMA v2 (DFS) | 61.0±1.8 | 58.8±0.5 | 45.6±0.9 | 60.3±1.3 | 53.5±1.8 | 48.1±1.5 | 54.6±1.3 |
| GPT-3.5-Turbo-1106 (CoT) | 50.4±0.5 | 45.1±1.4 | 50.8±0.3 | 48.7±0.8 | 42.1±0.4 | 55.7±0.0 | 48.8±0.6 |
| GPT-3.5-Turbo-1106 (DFS) | 62.8±0.3 | 63.9±1.2 | 65.6±0.3 | 56.5±0.7 | 56.9±1.2 | 67.2±1.3 | 62.2±0.8 |
| GPT-4-Turbo-Preview (CoT) | 52.8±1.3 | 56.6±0.9 | 51.9±0.5 | 51.9±1.0 | 52.8±0.8 | 52.5±0.0 | 53.1±0.8 |
| GPT-4-Turbo-Preview (DFS) | 59.2±0.5 | 61.7±0.7 | 65.7±1.0 | 55.6±0.6 | 55.2±0.4 | 66.1±4.3 | 60.6±1.3 |


[//]: # (**Solvable Pass Rate:**)

[//]: # (| **Method** | **I1 Instruction** | **I1 Category** | **I1 Tool** | **I2 Category** | **I2 Instruction** | **I3 Instruction** | **Average** |)

[//]: # (| --- | --- | --- | --- | --- | --- | --- | --- |)

[//]: # (| GPT-3.5-Turbo-0613  &#40;CoT&#41; | 55.9±1.0 | 50.8±0.8 | 55.9±1.0 | 44.1±0.8 | 36.2±0.4 | 51.4±1.5 | 49.1±1.0 |)

[//]: # (| GPT-3.5-Turbo-0613 &#40;DFS&#41; | 66.4±1.5 | 64.3±1.0 | 67.2±2.4 | 67.7±0.8 | 61.5±1.0 | 81.4±1.5 | 68.1±1.4 |)

[//]: # (| GPT-4-0613 &#40;CoT&#41; | 50.7±0.4 | 57.1±0.3 | 51.9±0.3 | 55.0±1.1 | 61.6±0.8 | 56.3±0.8 | 55.4±0.6 |)

[//]: # (| GPT-4-0613 &#40;DFS&#41; | 65.5±1.1 | 62.0±1.7 | 72.1±1.6 | **70.8±1.3** | **73.1±1.4** | 74.9±1.5 | 69.7±1.4 |)

[//]: # (| ToolLLaMA v2 &#40;CoT&#41; | 37.2±0.1 | 42.3±0.4 | 43.0±0.5 | 37.4±0.4 | 33.6±1.2 | 39.6±1.0 | 38.9±0.6 |)

[//]: # (| ToolLLaMA v2 &#40;DFS&#41; | 59.8±1.5 | 59.5±1.4 | 65.7±1.1 | 56.5±0.3 | 47.6±0.4 | 62.8±1.9 | 58.7±1.1 |)

[//]: # (| GPT-3.5-Turbo-1106 &#40;CoT&#41; | 51.3±0.6 | 48.8±0.3 | 59.9±0.8 | 50.8±0.7 | 43.2±0.8 | 58.5±0.8 | 52.1±0.7 |)

[//]: # (| GPT-3.5-Turbo-1106 &#40;DFS&#41; | 67.8±0.9 | 67.2±0.3 | **72.9±0.7** | 63.2±1.0 | 70.9±0.4 | 77.6±0.8 | 69.9±0.7 |)

[//]: # (| GPT-4-Turbo-Preview &#40;CoT&#41; | 63.1±1.0 | 64.5±0.5 | 55.3±0.3 | 63.0±0.8 | 57.3±0.8 | 61.7±0.8 | 60.8±0.7 |)

[//]: # (| GPT-4-Turbo-Preview &#40;DFS&#41; | **70.8±1.0** | **71.1±0.7** | 70.4±1.2 | 70.4±1.3 | 71.7±0.4 | **84.7±1.7** | **73.2±1.1** |)

In this experiment, we run all models once, evaluate them three times, and take the average results. 


**Solvable Win Rate:** (Reference model: ChatGPT-CoT)
| **Method** | **I1 Instruction** | **I1 Category** | **I1 Tool** | **I2 Instruction** | **I2 Category** | **I3 Instruction** | **Average** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-3.5-Turbo-0613 (DFS) | 60.7 | 67.3 | 59.5 | 63.2 | 62.1 | 75.4 | 64.7 |
| GPT-4-0613 (CoT) | 54.6 | 58.8 | 58.2 | 75.5 | 60.5 | 62.3 | 61.7 |
| GPT-4-0613 (DFS) | 62.6 | 62.7 | 58.2 | 74.5 | 62.9 | 67.2 | 64.7 |
| ToolLLaMA v2 (CoT) | 41.7 | 45.1 | 32.3 | 52.8 | 46.8 | 26.2 | 40.8 |
| ToolLLaMA v2 (DFS) | 42.3 | 51.0 | 31.0 | 67.0 | 54.0 | 31.1 | 54.0 |
| GPT-3.5-Turbo-1106 (CoT) | 47.2 | 47.7 | 44.9 | 50.9 | 54.0 | 62.3 | 51.2 |
| GPT-3.5-Turbo-1106 (DFS) | 55.8 | 53.6 | 51.9 | 68.9 | 59.7 | 68.9 | 59.8 |
| GPT-4-Turbo-Preview (CoT) | 71.2 | 77.1 | 61.4 | 79.2 | 71.8 | 67.2 | 71.3 |
| GPT-4-Turbo-Preview (DFS) | **73.0** | **75.2** | **68.4** | **77.4** | **66.9** | **60.7** | **70.2** |
We run all models once against `GPT-3.5-Turbo-0613 + CoT` and evaluate them three times. We follow the ToolBench implementation to take the most frequent result for each query during evaluation.

## Acknowledgement
We thank Jingwen Wu and Yao Li for their contributions to experiments and result presentation. We also appreciate Yile Wang and Jitao Xu for their valuable suggestions during discussions.
 ## Citation
```
@misc{guo2024stabletoolbench,
      title={StableToolBench: Towards Stable Large-Scale Benchmarking on Tool Learning of Large Language Models}, 
      author={Zhicheng Guo and Sijie Cheng and Hao Wang and Shihao Liang and Yujia Qin and Peng Li and Zhiyuan Liu and Maosong Sun and Yang Liu},
      year={2024},
      eprint={2403.07714},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
``` 
