cd  toolbench/tooleval
export API_POOL_FILE=../../openai_key.json
export CONVERTED_ANSWER_PATH=../../data_example/model_predictions_converted
export SAVE_PATH=../../data_example/preference_results
export PASS_RATE_PATH=../../data_example/pass_rate_results
export REFERENCE_MODEL=virtual_chatgpt_cot
export CANDIDATE_MODEL=virtual_chatgpt_dfs
export EVAL_MODEL=gpt-3.5-turbo
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