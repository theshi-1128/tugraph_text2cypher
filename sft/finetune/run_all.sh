MODEL="/data/dylin/models/Qwen2.5-14B-Instruct"

# ./finetune.sh $MODEL ../sft-data/qwen_sft_merged_common_data_with_schema_pipeline2_clean1.jsonl common/output_qwen2.5_14B_common_20241111 16
# sleep 60

# ./finetune.sh $MODEL ../sft-data/qwen_sft_merged_yago_new_schema_with_schema_data_pipeline2.jsonl yoga/output_qwen2.5_14B_yoga_20241111 16
# sleep 60

# 从输出目录中加载最后一个LoRA检查点
COMMON_CHECKPOINT=$(ls -td common/output_qwen2.5_14B_common_20241111/checkpoint-* | head -n 1)
YOGA_CHECKPOINT=$(ls -td yoga/output_qwen2.5_14B_yoga_20241111/checkpoint-* | head -n 1)

# 改为绝对路径
COMMON_CHECKPOINT="/data/ldy/text2Cypher/sft/finetune/"$COMMON_CHECKPOINT
YOGA_CHECKPOINT="/data/ldy/text2Cypher/sft/finetune/"$YOGA_CHECKPOINT

echo "Common 最后一个检查点: $COMMON_CHECKPOINT"
echo "Yoga 最后一个检查点: $YOGA_CHECKPOINT"

# ./checkpoint_finetune.sh $MODEL ../sft-data/sft-common-qwen-format-with-schema-test-new.jsonl $COMMON_CHECKPOINT common/Qwen2.5_14B_common_from_lora_20241111 8
# sleep 60

./checkpoint_finetune.sh $MODEL ../sft-data/sft-yago-qwen-format-with-schema-test.jsonl $YOGA_CHECKPOINT yoga/Qwen2.5_14B_yoga_from_lora_20241111 8
sleep 10

# 从输出目录中加载最后一个LoRA检查点
COMMON_LR=$(ls -td common/Qwen2.5_14B_common_from_lora_20241111/checkpoint-* | head -n 1)
YOGA_LR=$(ls -td yoga/Qwen2.5_14B_yoga_from_lora_20241111/checkpoint-* | head -n 1)
COMMON_LR="/data/ldy/text2Cypher/sft/finetune/"$COMMON_LR
YOGA_LR="/data/ldy/text2Cypher/sft/finetune/"$YOGA_LR

cd ../inference/moe

OUTPUT_FILE1="output_answer_20241111-1.json"
OUTPUT_FILE2="output_answer_20241111_from_lora-1.json"

CUDA_VISIBLE_DEVICES=2,3 python predict_moe_lora.py $MODEL $COMMON_CHECKPOINT $YOGA_CHECKPOINT $OUTPUT_FILE1
sleep 10
CUDA_VISIBLE_DEVICES=2,3 python predict_moe_lora.py $MODEL $COMMON_LR $YOGA_LR $OUTPUT_FILE2
sleep 10

git add .
git commit -m "自动提交output"
git push gitee master
