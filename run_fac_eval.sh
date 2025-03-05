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