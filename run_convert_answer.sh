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
    --method DFS_woFilter_w2 \
    --output ${output_file}