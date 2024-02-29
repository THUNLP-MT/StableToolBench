cd  /ML-A100/team/mm/chengsijie/gzc/ToolBench/toolbench/tooleval
export CONVERTED_ANSWER_PATH=../../data/model_predictions_converted/
export SAVE_PATH=../../data/preference_results_gpt4
export PASS_RATE_PATH=../../data/pass_rate_results_gpt4
export REFERENCE_MODEL=virtual_chatgpt_cot_1_8080
# export CANDIDATE_MODEL=virtual_gpt-4-0613_dfs_1_8080
export API_POOL_FILE=/ML-A100/team/mm/chengsijie/gzc/STC/openai_key.json
export OPENAI_API_BASE="https://api.01ww.xyz/v1" 
export OPENAI_API_KEY=openchat
export EVAL_MODEL=gpt-4-turbo-preview
mkdir -p ${SAVE_PATH}


# for candidate_model in virtual_gpt-4-0613_dfs_1_8080 virtual_gpt-4-0613_cot_1_8080 virtual_gpt-3.5-turbo-1106_cot_1_8082 virtual_gpt-3.5-turbo-1106_dfs_1_8082 virtual_gpt-4-turbo-preview_cot_1_8082 virtual_gpt-4-turbo-preview_dfs_1_8082; do
for candidate_model in virtual_toolllama_cot_8082 virtual_toolllama_dfs_8082; do
echo "<---------------candidate_model: ${candidate_model}------------------>"
export CANDIDATE_MODEL=${candidate_model}
python eval_preference.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --reference_model ${REFERENCE_MODEL} \
    --output_model ${CANDIDATE_MODEL} \
    --test_ids /ML-A100/team/mm/chengsijie/gzc/ToolBench/check_task_solvable/solvable_queries2/test_query_ids/ \
    --save_path ${SAVE_PATH} \
    --pass_rate_result_path ${PASS_RATE_PATH} \
    --max_eval_threads 10 \
    --use_pass_rate true \
    --evaluate_times 3 --overwrite
done