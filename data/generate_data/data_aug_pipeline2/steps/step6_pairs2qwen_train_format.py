import os
import json
import re

# 文件夹路径
folder_path = './gen_cyphers/yago_new_schema/1'

# 创建输出文件夹的函数
# def create_output_folder(db_name, hard):
#     output_folder = os.path.join(f"./qwen-pairs/{db_name}/{hard}")
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#     return output_folder

def create_output_folder_same_distribution(db_name):
    output_folder = os.path.join(f"./qwen-pairs/yago_new_schema/1")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

# 创建输出文件
# 遍历文件夹中的所有txt文件
for filename in os.listdir(folder_path):
    if os.path.splitext(filename)[1] != ".txt":
        continue
    basename = os.path.splitext(filename)[0]

    # 分割文件名
    params = basename.split('_')
    # 获取最后三个参数
    db_name = params[-1]
    if db_name == "body":
        # num = params[-5]
        # hard = params[-4]
        num = params[-4]
        db_name = "the_three_body"
    else:
        num = params[-3]
        hard = params[-2]

    file_path = os.path.join(folder_path, filename)
    query_path = f"./gen_questions/yago_new_schema/1/step4_gen_questions_random_distribution_res_{num}_{hard}_{db_name}.txt"
    # query_path = f"./gen_template_pairs/placeholders/step5_use_tricks_gen_questions_res_{num}_{hard}_{db_name}.txt"

    # 提取Question和Cypher
    with open(query_path, 'r', encoding='utf-8') as file2:
        content = file2.read()
        questions = re.findall(r'Question:\s*(.*)', content)
        questions = [q.strip('"') for q in questions]

    queries = []
    cypher_pattern = re.compile(r"\d+\.\s*Cypher:")  # 匹配 'X. Cypher:'，X 是任意数字
    with open(file_path, 'r', encoding='utf-8') as file:
        query = []
        lines = file.readlines()

        inside_query = False
        for line in lines:
            line = line.strip()
            if cypher_pattern.match(line):  # 找到 Cypher 的标记行
                inside_query = True
                query = []  # 清空当前 query
            elif inside_query:
                if not line or line.startswith("```"):  # 结束查询遇到空行或'''
                    if query:  # 确保 query 不为空
                        query_text = " ".join(query).strip()
                        # 检查是否以 ''' 结束，如果是则去掉
                        # if query_text.endswith("```"):
                        #     query_text = query_text[:-3].strip()
                        queries.append(query_text)  # 将查询拼接成一行
                    inside_query = False
                else:
                    query.append(line)  # 将当前行加入到 query 中
    if len(queries) != 3:
        print(filename)
        print(len(queries))
        # 如果文件结尾是 Cypher 查询，且没有遇到 '''，需要最后追加查询
        # if query:
        #     query_text = " ".join(query).strip()
        #     queries.append(query_text)

    # 根据不同的 db_name 和 hard 创建对应的文件夹
    # output_folder = create_output_folder_same_distribution(db_name, hard)
    output_folder = create_output_folder_same_distribution(db_name)

    # 合并qwen_format
    for (question, query) in zip(questions,queries):
        if question != "" and query != "":
            # 构建JSON对象
            json_object = {
                "type": "chatml",
                "messages": [
                    {"role": "system", "content": "你是一个自然语言翻译Cypher语句的专家，请你把用户的自然语言问题翻译成Cypher语句"},
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": query}
                ],
                "source": "self-made"
            }

            # 写入到对应的文件夹和文件
            output_file = os.path.join(output_folder, f"qwen_train_{db_name}.jsonl")
            # output_file = os.path.join(output_folder, f"qwen_train_{db_name}_{hard}.jsonl")
            with open(output_file, 'a', encoding='utf-8') as jsonl_file:
                jsonl_file.write(json.dumps(json_object, ensure_ascii=False) + '\n')

