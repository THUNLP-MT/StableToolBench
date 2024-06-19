export TOOLBENCH_KEY=""

export OPENAI_KEY=""
export OPENAI_API_BASE=""
export PYTHONPATH=./
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy

export GPT_MODEL="gpt-3.5-turbo-16k"
export SERVICE_URL="http://localhost:8080/virtual"

export OUTPUT_DIR="data/answer/virtual_chatgpt_cot"
group=G1_instruction
mkdir -p $OUTPUT_DIR; mkdir -p $OUTPUT_DIR/$group
python toolbench/inference/qa_pipeline_multithread.py \
    --tool_root_dir toolenv/tools \
    --backbone_model chatgpt_function \
    --chatgpt_model $GPT_MODEL \
    --openai_key $OPENAI_KEY \
    --max_observation_length 1024 \
    --method CoT@1 \
    --input_query_file solvable_queries/test_instruction/${group}.json \
    --output_answer_file $OUTPUT_DIR/$group \
    --toolbench_key $TOOLBENCH_KEY \
    --num_thread 5 --overwrite