cd  toolbench/tooleval
export API_POOL_FILE=../../openai_key.json
export CONVERTED_ANSWER_PATH=../../data/model_predictions_converted
export SAVE_PATH=../../data/pass_rate_results
export OPENAI_API_BASE="https://api.01ww.xyz/v1" 
export OPENAI_API_KEY=openchat
mkdir -p ${SAVE_PATH}
export CANDIDATE_MODEL=virtual_gpt-3.5-turbo-0613_cot
export EVAL_MODEL=gpt-4-turbo-preview
mkdir -p ${SAVE_PATH}/${CANDIDATE_MODEL}
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy

python eval_pass_rate.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --save_path ${SAVE_PATH}/${CANDIDATE_MODEL} \
    --reference_model ${CANDIDATE_MODEL} \
    --test_ids ../../solvable_queries/test_query_ids \
    --max_eval_threads 35 \
    --evaluate_times 3 \
    --test_set  G1_instruction \
    --overwrite