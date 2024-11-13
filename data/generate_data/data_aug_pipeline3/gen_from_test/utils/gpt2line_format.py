import json

# 输入和输出文件路径
input_file_path = 'temp_tempate2pairs_common.json'  # 你的源文件名
output_file_path = 'sft_output_common.jsonl'  # 输出文件名

# 打开输入文件，逐行读取
with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        # 解析每行 JSON 数据
        data = json.loads(line)
        
        # 提取 answers 列表中的每个 question-cypher 对
        extracted_pairs = [{"question": item["question"], "cypher": item["cypher"]} for item in data["answers"]]
        
        # 将提取的对逐行写入新文件
        for pair in extracted_pairs:
            json.dump(pair, outfile, ensure_ascii=False)
            outfile.write('\n')  # 每行一个 JSON 对象

print("数据提取完成并已写入输出文件。")
