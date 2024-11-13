import json
import torch
from tqdm import tqdm
from transformers import AutoTokenizer
from vllm.lora.request import LoRARequest
from vllm import LLM, SamplingParams
import sys

#########################################################################################

# model_name = "/data/ldy/kg-llm/models/Qwen2.5-14B-Instruct/"

# commonLR_path = "/data/ldy/text2Cypher/sft/finetune/common/Qwen2.5_14B_common_from_lora_20241111/checkpoint-95"
# yagoLR_path = "/data/ldy/text2Cypher/sft/finetune/yoga/Qwen2.5_14B_yoga_from_lora_20241111/checkpoint-90"

# output_file = "/data/ldy/text2Cypher/sft/inference/moe/output_answers-11-11-lora-1.json"


model_name = sys.argv[1]
commonLR_path = sys.argv[2]
yagoLR_path = sys.argv[3]
output_file = sys.argv[4]

#########################################################################################


llm_model = LLM(
    model_name,
    enable_lora=True,
    max_lora_rank=64,
    tensor_parallel_size=2,
    gpu_memory_utilization=0.95,
    dtype=torch.float16
)

num_gpus = 2  # Change this to the number of GPUs you have
tokenizer = AutoTokenizer.from_pretrained(model_name)

commonLR = LoRARequest("common", 1, commonLR_path)
yagoLR = LoRARequest("yago", 2, yagoLR_path)

def predict(messages, model, lora, tokenizer):
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Set sampling parameters for generation
    sampling_params = SamplingParams(max_tokens=1024)

    # Generate the output using vLLM
    output = model.generate(prompt, sampling_params, lora_request=lora)

    response = output[0].outputs[0].text.strip()
    return response


# 读取测试集文件
def load_test_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    

def predict_all(test_data, model, tokenizer):
    with open('./prompts/yoga_prompt.txt', 'r', encoding='utf-8') as f:
        yoga_prompt = f.read()
    with open('./prompts/common_prompt.txt', 'r', encoding='utf-8') as f:
        common_prompt = f.read()
    results = []
    for index, data in tqdm(enumerate(test_data), total=len(test_data), desc="Predicting"):
        question = data['question']
        db_id = data['db_id']
        if db_id == "yago":
            messages = [
                {"role": "system",
                "content": yoga_prompt},
                {"role": "user", "content": question}
            ]
            answer = predict(messages, model, yagoLR, tokenizer)
        elif db_id == "common":
            messages = [
                {"role": "system",
                "content": common_prompt},
                {"role": "user", "content": question}
            ]
            answer = predict(messages, model, commonLR, tokenizer)
        results.append({"index": str(index), "answer": answer})

    return results


# 保存推理结果到输出文件
def save_results(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

test_file = "/data/ldy/text2Cypher/data/given_data/test_cypher.json"

# 主流程
def main(test_file, output_file, model, tokenizer):
    # 加载测试数据
    test_data = load_test_data(test_file)

    # 执行推理
    results = predict_all(test_data, model, tokenizer)

    # 保存结果
    save_results(results, output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main(test_file, output_file, llm_model, tokenizer)
