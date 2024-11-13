import json

# 读取原始文件并转换格式
input_file = "sft_output_common.jsonl"  # 原始jsonl文件路径
output_file = "sft-common-qwen-format.jsonl"  # 输出jsonl文件路径

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        # 读取并解析每一行的JSON数据
        data = json.loads(line.strip())
        
        # 构建新的格式
        new_data = {
            "type": "chatml",
            "messages": [
                {"role": "system", "content": "你是一个自然语言翻译Cypher语句的专家，请你把用户的自然语言问题翻译成Cypher语句"},
                {"role": "user", "content": data["question"]},
                {"role": "assistant", "content": data["cypher"]}
            ],
            "source": "self-made"
        }
        
        # 写入新的JSONL文件
        outfile.write(json.dumps(new_data, ensure_ascii=False) + '\n')

print(f"转换完成，结果已保存至 {output_file}")
