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

<!-- <div align="center">
<img src="https://cdn.discordapp.com/attachments/941582479117127680/1111543600879259749/20230526075532.png" width="350px">
</div> -->

🔨Welcome to StableToolBench. Faced with the instability of Tool Learning benchmarks, especially ToolBench (Qin et al., 2023), we developed this new benchmark aiming to balance the stability and reality.
<!-- 
**💁‍♂️💁💁‍♀️ Join Us on [Discord](https://discord.gg/NScFnpMuRQ)!** -->

<!-- *Read this in [中文](README_ZH.md).* -->

## Features
- **Virtual API System**, which comprises a caching system and API simulators. The caching system stores API call responses to ensure consistency, while the API simulators, powered by LLMs, are used for unavailable APIs.
- **A New Set of Solvable Queries**. Query solvability is hard to determine on the fly, causing sigificant randomness and instability. In StableToolBench, we use state-of-the-art LLMs to determine task solvability to filter queries beforehand. 
- **Stable Evaluation System**: Implements a two-phase evaluation process using GPT-4 as an automatic evaluator. It involves judging the solvability of tasks and employing metrics like Solvable Pass Rate (SoPR) and Solvable Win Rate (SoWR).


### Next Steps

## The Virtual API Server

👐ToolBench is intended solely for research and educational purposes and should not be construed as reflecting the opinions or views of the creators, owners, or contributors of this dataset. It is distributed under Apache License 2.0. Below is the statistics of the data :

| Tool Nums | API Nums | Instance Nums | Real API Call | Reasoning Traces |
|-----------|----------|---------------|---------------|------------------|
| 3451      | 16464    | 126486         | 469585         | 4.0              |

We crawl 16000+ real-world APIs from [RapidAPI](https://rapidapi.com/hub), and curate realistic human instructions that involve them. Below we present a hierarchy of RapidAPI and our instruction generation process.


ToolBench contains both single-tool and multi-tool scenarios. The multi-tool scenarios can be further categorized into intra-category multi-tool and intra-collection multi-tool. We utilize DFSDT method for all scenarios to our data creation. Here is an illustration for the data creation process using DFSDT method:


### API Simulation

### Cache
 Please download our dataset using the following link: [Google Drive](https://drive.google.com/drive/folders/1yBUQ732mPu-KclJnuQELEhtKakdXFc3J) or [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/c9e50625743b40bfbe10/). *Notice that `data_0801` is the old version data.*
The file structure is as follows:
```
├── /data/
│  ├── /instruction/
│  ├── /answer/
│  ├── /toolenv/
│  ├── /retrieval/
│  ├── /test_instruction/
│  ├── /test_query_ids/
│  ├── /retrieval_test_query_ids/
│  ├── toolllama_G123_dfs_train.json
│  └── toolllama_G123_dfs_eval.json
├── /reproduction_data/
│  ├── /chatgpt_cot/
│  ├── /chatgpt_dfs/
│  ├── ...
│  └── /toolllama_dfs/
```
Here are some descriptions for the `data` directory:
- `instruction` and `answer`: The instruction data and solution path annotation data. `G1`,`G2`, `G3` refers to single-tool, intra-category multi-tool and intra-collection multi-tool data respectively. We also have an [Atlas Explorer](https://atlas.nomic.ai/map/58aca169-c29a-447a-8f01-0d418fc4d341/030ddad7-5305-461c-ba86-27e1ca79d899) for visualization.
- `toolenv`: The tool environment related data, containing API jsons, API codes and API example responses.
- `retrieval`: The data used for tool retrieval is included in this directory.
- `test_instruction` and `test_query_ids`: We sample 200 instances from every test set. The `test_instruction` directory contains test queries for each test set, and the `test_query_ids` contains query ids of the test instances in each test set.
- `retrieval_test_query_ids`: This directory contains query ids of the test instances for retriever.
- `toolllama_G123_dfs_train.json` and `toolllama_G123_dfs_eval.json`: Preprocessed data that can be used to train toolllama directly and reproduce our results. For preprocessing details, we split the G1, G2 and G3 data into train, eval and test parts respectively and combine the train data for training in our main experiments.

*Please make sure you have downloaded the necessary data and put the directory (e.g. `data/`) under `ToolBench/`, so that the following bash scripts can navigate to the related data.*
<!-- 
## 🤖Model

We release the [ToolLLaMA-2-7b-v2](https://huggingface.co/ToolBench/ToolLLaMA-2-7b-v2) which is trained on the latest version data, and [ToolLLaMA-7b-v1](https://huggingface.co/ToolBench/ToolLLaMA-7b-v1), [ToolLLaMA-7b-LoRA-v1](https://huggingface.co/ToolBench/ToolLLaMA-7b-LoRA-v1) which are trained on the 0801 version data. All models are trained on the released dataset in a multi-task fashion. We also release the [tool retriever](https://huggingface.co/ToolBench/ToolBench_IR_bert_based_uncased) trained under our experimental setting. -->

## Inference With Our StableToolBench Server
Please fill out the [form](https://forms.gle/oCHHc8DQzhGfiT9r6) first and after reviewing we will send you the toolbench key. Then prepare your toolbench key by:
```bash
export TOOLBENCH_KEY="your_toolbench_key"
```

### For OpenAI Models
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

To use Text-Davinci-003, run:
```bash
export TOOLBENCH_KEY=""
export OPENAI_KEY=""
export PYTHONPATH=./
python toolbench/inference/qa_pipeline.py \
    --tool_root_dir data/toolenv/tools/ \
    --backbone_model davinci \
    --openai_key $OPENAI_KEY \
    --max_observation_length 1024 \
    --method DFS_woFilter_w2 \
    --input_query_file data/test_instruction/G1_instruction.json \
    --output_answer_file davinci_dfs_inference_result \
    --toolbench_key $TOOLBENCH_KEY
```
## Setting up and running the interface
ToolBench contains a Web UI based on [Chatbot UI](https://github.com/mckaywrigley/chatbot-ui), forked to include the use of tools in the interface. It comes in two parts: the backend server, and [chatbot-ui-toolllama](https://github.com/lilbillybiscuit/chatbot-ui-toolllama). Here is a [video demo](assets/toolbench-demo.mp4).


## StableToolEval

<!-- By fine-tuning LLaMA on ToolBench, we obtain **ToolLLaMA**. Considering that human evaluation can be time-consuming, we follow [AlpacaEval](https://tatsu-lab.github.io/alpaca_eval/) to develop an efficient machine evaluator **ToolEval**, which incorporates two evaluation metrics:
 - **Pass Rate**: Calculates the proportion of successfully completing an instruction within limited OpenAI API calls. 
 - **Preference**: Measured by comparing two answers (action sequences) for a given instruction. We pre-define a set of criteria for a better answer, which are organized as prompts for ChatGPT. We provide the test instruction and two candidate answers to the evaluator and obtain its preference. We evaluate each answer pair multiple times to improve the reliability of our system. Then we calculate the **Win Rate** (percentage of being preferred by the evaluator). More details can be found in our paper.

To validate the reliability of ChatGPT evaluator in both pass rate and win rate, we sample among four different methods (ChatGPT+ReACT, ChatGPT+DFSDT, ToolLLaMA+DFSDT and GPT4+DFSDT) to obtain solution pairs for 300 test instructions for each method. Then we engage humans to annotate the pass rate for ChatGPT+DFSDT, ToolLLaMA+DFSDT and GPT4+DFSDT, and the win rate among ChatGPT+ReACT and ChatGPT+DFSDT.
Our ChatGPT evaluator demonstrates a high agreement of **87.1%** in pass rate and **80.3%** in win rate with human annotators. This result shows that our evaluator generates highly similar evaluation results to humans and can be viewed as a credible evaluator who simulates human evaluation on pass rate and win rate.

More details about ToolEval can be found in our paper. -->

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