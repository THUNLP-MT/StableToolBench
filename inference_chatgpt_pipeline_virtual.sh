export TOOLBENCH_KEY="xud2dQdMNE8MRlkwBTe5DYB0DkktPi1uiCnyteptzmg3gS7Bbz"

export OPENAI_KEY="openchat"
export OPENAI_API_BASE="https://api.01ww.xyz/v1" 
export PYTHONPATH=./
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy

export GPT_MODEL="gpt-3.5-turbo-0613"
export SERVICE_URL="http://localhost:8080/virtual"

export OUTPUT_DIR="data/answer/virtual_${GPT_MODEL}_cot"
group=G1_instruction
mkdir -p $OUTPUT_DIR; mkdir -p $OUTPUT_DIR/$group
python toolbench/inference/qa_pipeline_multithread.py \
    --tool_root_dir /home/gzc/disk5/gzc/ToolBench/data/toolenv/tools \
    --backbone_model chatgpt_function \
    --openai_key $OPENAI_KEY \
    --max_observation_length 1024 \
    --method CoT@1 \
    --input_query_file /home/gzc/disk5/gzc/StableToolBench/solvable_queries/test_instruction/${group}.json \
    --output_answer_file $OUTPUT_DIR/$group \
    --toolbench_key $TOOLBENCH_KEY \
    --num_thread 1 --overwrite 