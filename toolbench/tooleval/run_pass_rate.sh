cd  /ML-A100/team/mm/chengsijie/gzc/ToolBench/toolbench/tooleval
export CONVERTED_ANSWER_PATH=../../data/model_predictions_converted
# export CONVERTED_ANSWER_PATH=../../data/reproduction_data/model_predictions_converted/ \
export SAVE_PATH=../../data/pass_rate_results_gpt4
# export SAVE_PATH=../../data/reproduction_data/pass_rate_results/ \
# export CANDIDATE_MODEL=toolllama_dfs_fail0.1

export API_POOL_FILE=/ML-A100/team/mm/chengsijie/gzc/STC/openai_key.json
export OPENAI_API_BASE="https://api.01ww.xyz/v1" 
export OPENAI_API_KEY=openchat
mkdir -p ${SAVE_PATH}

# for method in cot dfs; do
# for model in chatgpt gpt-4-0613; do
# # model=gpt-3.5-turbo-1106
# # model=chatgpt
# export EVAL_MODEL=gpt-4-turbo-preview
# for run_times in 1; do
# for port in 8086 8087 8088; do #8080 8083 8084 8085 8086 8087 8088
# echo "port: ${port} method: ${method} model: ${model} run_times: ${run_times}"
#     export CANDIDATE_MODEL=virtual_${model}_${method}_${run_times}_${port}
#     mkdir -p ${SAVE_PATH}/${CANDIDATE_MODEL}
#     python eval_pass_rate.py \
#         --converted_answer_path ${CONVERTED_ANSWER_PATH} \
#         --save_path ${SAVE_PATH}/${CANDIDATE_MODEL} \
#         --reference_model ${CANDIDATE_MODEL} \
#         --test_ids /ML-A100/team/mm/chengsijie/gzc/ToolBench/check_task_solvable/solvable_queries2/test_query_ids \
#         --max_eval_threads 20 \
#         --evaluate_times 3 \
#         --test_set  G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction # G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
# done
# done
# done
# done
