#!/bin/bash
export CUDA_DEVICE_MAX_CONNECTIONS=1

export CUDA_VISIBLE_DEVICES=2,3

GPUS_PER_NODE=$(python -c 'import torch; print(torch.cuda.device_count())')
NNODES=${NNODES:-1}
NODE_RANK=${NODE_RANK:-0}
MASTER_ADDR=${MASTER_ADDR:-localhost}
MASTER_PORT=${MASTER_PORT:-6003}


# MODEL="/data/ldy/kg-llm/models/Qwen2.5-14B-Instruct"
# DATA="/data/ldy/text2Cypher/sft/sft-data/sft-yago-qwen-format-with-schema-test-with-schema.jsonl"
# LORA_PATH="/data/ldy/text2Cypher/sft/finetune/loras/output_qwen2_5_14B_yoga_20241105-1/checkpoint-415"
# OUTPUT_DIR="yoga/Qwen2.5_14B_yoga_from_lora_20241107-1"

########################参数#######################################
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <model_path> <data_path> <lora_path> <output_dir> <batch_size>"
    exit 1
fi

MODEL=$1
DATA=$2
LORA_PATH=$3
OUTPUT_DIR=$4
BS=$5

echo "Model path: $MODEL"
echo "Data path: $DATA"
echo "Lora path: $LORA_PATH"
echo "Output directory: $OUTPUT_DIR"
echo "Batch size: $BS"
#####################################################################


DS_CONFIG_PATH="ds_config_zero3.json"
USE_LORA=True
Q_LORA=False


DISTRIBUTED_ARGS="
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --node_rank $NODE_RANK \
    --master_addr $MASTER_ADDR \
    --master_port $MASTER_PORT\
"

CUDA_VISIBLE_DEVICES=2,3 torchrun $DISTRIBUTED_ARGS finetune.py \
    --model_name_or_path $MODEL \
    --data_path $DATA \
    --fp16 True \
    --output_dir $OUTPUT_DIR \
    --num_train_epochs 5 \
    --per_device_train_batch_size $BS \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 2 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 10 \
    --save_total_limit 10 \
    --learning_rate 1e-4 \
    --weight_decay 0.01 \
    --adam_beta2 0.95 \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --report_to "none" \
    --model_max_length 512 \
    --lazy_preprocess True \
    --use_lora ${USE_LORA} \
    --q_lora ${Q_LORA} \
    --lora_weight_path ${LORA_PATH} \
    --gradient_checkpointing \
    --deepspeed ${DS_CONFIG_PATH}
