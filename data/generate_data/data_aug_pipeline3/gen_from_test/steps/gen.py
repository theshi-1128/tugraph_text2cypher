import json
import openai
import time
from tqdm import tqdm
import os
import random
from openai import OpenAI

from openai import OpenAIError, RateLimitError, APIError, Timeout
client = OpenAI()




import time
from openai import OpenAIError

def call_gpt4o(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},  # 系统消息
        {"role": "user", "content": prompt}  # 用户提供的 prompt
    ]

    # 异常处理
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # 指定模型名称
                messages=messages,
                response_format ={
                    "type": "json_schema",
                    "json_schema": {
                        # "name": "reasoning_schema",
                        "name": "answer_schema",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                # "reasoning_steps": {
                                #     "type": "array",
                                #     "items": {
                                #         "type": "string"
                                #     },
                                #     "description": "推理过程步骤，解释如何得出最终结论,中文回答。"
                                # },
                                "answer": {
                                    "type": "object",  # 修改answer为object类型
                                    "properties": {
                                        "question": {"type": "string", "description": "生成的自然语言问题template。"},
                                        "cypher": {"type": "string", "description": "生成的 Cypher 查询语句template。"}
                                    },
                                    "required": ["question", "cypher"],  # 确保answer包含两个部分
                                    "description": "The final answer in JSON format.",
                                    "additionalProperties": False  # 显式设置 additionalProperties 为 False
                                }
                            },
                            "required": ["answer"],
                            # "required": ["reasoning_steps", "answer"],
                            "additionalProperties": False  # 显式设置 additionalProperties 为 False
                        }
                    }
                },
                max_tokens=500,  # 设置最大返回 token 数量
                n=1,  # 生成一个响应
                temperature=0.7  # 调整生成文本的多样性
            )

            # 提取并返回响应内容
            return response.choices[0].message.content
        except OpenAIError as e:
            print(f"Error: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # 如果出错则等待10秒后重试

# def call_gpt4o(prompt):
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},  # 系统消息
#         {"role": "user", "content": prompt}  # 用户提供的 prompt
#     ]

#     # 异常处理
#     while True:
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4o",  # 指定模型名称
#                 messages=messages,
#                 # response_format ={
#                 #     "type": "json_schema",
#                 #     "json_schema": {
#                 #         # "name": "reasoning_schema",
#                 #         "name": "answer_schema",
#                 #         "strict": True,
#                 #         "schema": {
#                 #             "type": "object",
#                 #             "properties": {
#                 #                 # "reasoning_steps": {
#                 #                 #     "type": "array",
#                 #                 #     "items": {
#                 #                 #         "type": "string"
#                 #                 #     },
#                 #                 #     "description": "推理过程步骤，解释如何得出最终结论,中文回答。"
#                 #                 # },
#                 #                 "answer": {
#                 #                     "type": "object",  # 修改answer为object类型
#                 #                     "properties": {
#                 #                         "question": {"type": "string", "description": "生成的自然语言问题。"},
#                 #                         "cypher": {"type": "string", "description": "生成的 Cypher 查询语句。"}
#                 #                     },
#                 #                     "required": ["question", "cypher"],  # 确保answer包含两个部分
#                 #                     "description": "The final answer in JSON format.",
#                 #                     "additionalProperties": False  # 显式设置 additionalProperties 为 False
#                 #                 }
#                 #             },
#                 #             "required": ["answer"],
#                 #             # "required": ["reasoning_steps", "answer"],
#                 #             "additionalProperties": False  # 显式设置 additionalProperties 为 False
#                 #         }
#                 #     }
#                 # },
#                 max_tokens=200,  # 设置最大返回 token 数量
#                 n=1,  # 生成一个响应
#                 temperature=0.7  # 调整生成文本的多样性
#             )

#             # 提取并返回响应内容
#             return response.choices[0].message.content
#         except OpenAIError as e:
#             print(f"Error: {e}. Retrying in 10 seconds...")
#             time.sleep(10)  # 如果出错则等待10秒后重试

with open("/data/text2cypher/sft/inference/moe/updated_file2.json","r",encoding="utf-8") as f_test:
    train_data = json.load(f_test)
    # train_data = []
    # # 逐行读取jsonl文件
    # # for line in f_test:
    # #     # print(line)
    # #     # 将每一行解析为JSON对象（字典）
    # #     try:
    # #         # 尝试解析每一行的JSON数据
    # #         data = json.loads(line.strip())
    # #         # 正常情况下打印解析成功的内容
    # #     except json.JSONDecodeError as e:
    # #         # 打印出出现错误的行和错误信息
    # #         print(f"JSONDecodeError: {e} in line: {line}")
    # #     # 处理或打印数据
    # train_data.append(data)

# with open('../test_like_data/schema_in_text/common.txt','r',encoding='utf-8') as f0:
#     extracted_schema0 = f0.read()

# with open('../../schema/movie.json', 'r', encoding='utf-8') as f1:
#     extracted_schema1 = f1.read()
#
# with open('../../schema/finbench.json', 'r', encoding='utf-8') as f2:
#     extracted_schema2 = f2.read()

# with open('../../schema/yago.json', 'r', encoding='utf-8') as f3:
#     extracted_schema3 = f3.read()

# with open('../../schema/the_three_body.json', 'r', encoding='utf-8') as f4:
#     extracted_schema4 = f4.read()

# extracted_schema = [extracted_schema0, extracted_schema1, extracted_schema2, extracted_schema3, extracted_schema4]
# extracted_schema = [extracted_schema0]

with open('gen_template_prompt.txt', 'r', encoding='utf-8') as f5:
    prompt = f5.read()

for item in train_data:
    idx = int(item.get("index"))
    if idx >=45 and idx <= 84:
        question = item.get("question")
        cypher = item.get("right_answer")
        output = call_gpt4o(prompt.replace('{question}',question).replace('cypher',cypher))

        with open(f"temp_template_yago.json", "a", encoding="utf-8") as f7:
            json_output = json.dumps(output, ensure_ascii=False)  # 转换为 JSON 字符串，保留非 ASCII 字符
            f7.write(json_output)
            f7.write("\n")

# with tqdm(total = 4806) as pbar:
#     for id, schema in enumerate(extracted_schema):
#         if id == 0:
#             name = "common"
#         # elif id == 1:
#         #     name = "yago"
#         # elif id == 2:
#         #     name = "finbech"
#         # elif id == 3:
#         #     name = "movie"
#         # elif id == 4:
#         #     name = "the_three_body"
#         for rule in test_clean:
#             for item in train_data:
#                 cur_prompt = prompt.replace('{schema}', schema).replace('{train_data}', str(item)) \
#                     .replace('{problem}',rule)

#                 output = call_gpt4o(cur_prompt)

#                 with open(f"temp_as.json", "a", encoding="utf-8") as f7:
#                     json_output = json.dumps(output, ensure_ascii=False)  # 转换为 JSON 字符串，保留非 ASCII 字符
#                     f7.write(json_output)
#                     f7.write("\n")
#                     pbar.update(1)
#             break


