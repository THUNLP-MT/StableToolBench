cd /ML-A100/team/mm/chengsijie/gzc/ToolBench/toolbench/tooleval
export RAW_ANSWER_PATH=../../data/answer
export CONVERTED_ANSWER_PATH=../../data/model_predictions_converted

# export METHOD=CoT@1
# export MODEL_NAME=virtual_toolllama_cot_8082
# mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
# for test_set in G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
# do
#     answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
#     output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
    
#     python convert_to_answer_format.py\
#         --answer_dir ${answer_dir} \
#         --method ${METHOD} \
#         --output ${output_file}
# done


# export METHOD=DFS_woFilter_w2
# for run_times in 1 2 3; do
#     export MODEL_NAME=virtual_chatgpt_dfs_${run_times}
#     mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
#     for test_set in G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
#     do
#         answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
#         output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
        
#         python convert_to_answer_format.py\
#             --answer_dir ${answer_dir} \
#             --method ${METHOD} \
#             --output ${output_file}
#     done
# done

# export METHOD=DFS_woFilter_w2
# for run_times in 1 2 3; do
#     export MODEL_NAME=virtual_chatgpt_dfs_${run_times}
#     mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
#     for test_set in G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
#     do
#         answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
#         output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
        
#         python convert_to_answer_format.py\
#             --answer_dir ${answer_dir} \
#             --method ${METHOD} \
#             --output ${output_file}
#     done
# done

# export METHOD=DFS_woFilter_w2
# export MODEL_NAME=virtual_toolllama_dfs_8082
# mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
# for test_set in G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
# do
#     answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
#     output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
    
#     python convert_to_answer_format.py\
#         --answer_dir ${answer_dir} \
#         --method ${METHOD} \
#         --output ${output_file}
# done


# export METHOD=CoT@1 #CoT@1 #DFS_woFilter_w2 #CoT@1
# for FAILURE_RATE in 0.05 0.1 0.5; do
#     export MODEL_NAME=toolllama_cot_fail${FAILURE_RATE}_v3
#     mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
#     for test_set in G1_instruction #G1_category G1_tool G2_category G2_instruction G3_instruction
#     do
#         answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
#         output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
        
#         python convert_to_answer_format.py\
#             --answer_dir ${answer_dir} \
#             --method ${METHOD} \
#             --output ${output_file}
#     done
# done
# export METHOD=DFS_woFilter_w2
# for FAILURE_RATE in 0 0.1 0.2 0.5; do
# for run_times in 1; do
#     echo "Running failure rate: $FAILURE_RATE and run times: $run_times and method: $METHOD"
#     export MODEL_NAME=gpt-4-0613_dfs_fail${FAILURE_RATE}_${run_times}_v5
#     mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
#     for test_set in G1_instruction
#     do
#         answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
#         output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
        
#         python convert_to_answer_format.py\
#             --answer_dir ${answer_dir} \
#             --method ${METHOD} \
#             --output ${output_file}
#     done
# done
# done

# export METHOD=DFS_woFilter_w2
# export MODEL="gpt-3.5-turbo-16k-0613"
# for param in 01 02 05; do
#     echo "Running Model: $MODEL and method: $METHOD"
#     export MODEL_NAME=virtual_${MODEL}_dfs_parameter${param}_v2
#     mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
#     for test_set in G1_instruction
#     do
#         answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
#         output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
        
#         python convert_to_answer_format.py\
#             --answer_dir ${answer_dir} \
#             --method ${METHOD} \
#             --output ${output_file}
#     done
# done



export method_in_path=dfs
if [ ${method_in_path} == "dfs" ]; then
    export METHOD=DFS_woFilter_w2
else
    export METHOD=CoT@1
fi
# model=gpt-3.5-turbo-1106
model=gpt-4-turbo-preview
for port in 8082 8083 8084 8085 8086 8087 8088; do
for run_times in 1; do
echo "Running model: $model and method: $METHOD and port: $port"
    export MODEL_NAME=virtual_${model}_${method_in_path}_${run_times}_${port}
    mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
    for test_set in G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
    do
        answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
        output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
        
        python convert_to_answer_format.py\
            --answer_dir ${answer_dir} \
            --method ${METHOD} \
            --output ${output_file}
    done
done
done
