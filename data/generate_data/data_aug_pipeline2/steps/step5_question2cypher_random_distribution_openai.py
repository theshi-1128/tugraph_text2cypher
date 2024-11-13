import json
import tiktoken
import openai
from tqdm import tqdm
import time
from openai import OpenAI
from openai import OpenAIError, RateLimitError, APIError, Timeout
client = OpenAI()
# 设置你的 API 密钥
# model = "gpt-4"
# 获取指定模型的 tokenizer
# encoding = tiktoken.encoding_for_model(model)

# 调用 GPT-4o 模型的函数
def call_gpt4o(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},  # 系统消息
        {"role": "user", "content": prompt}  # 用户提供的 prompt
    ]
    # 计算每条消息的 token 数量dd
    # token_count = sum([len(encoding.encode(message["content"])) for message in messages])
    # print(token_count)

    # 异常处理
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # 指定模型名称
                messages=messages,
                max_tokens=2000,  # 设置最大返回 token 数量
                n=1,  # 生成一个响应
                stop=None,  # 设置停止条件
                temperature=0.7  # 调整生成文本的多样性
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(f"Error: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # 如果出错则等待10秒后重试

with open('../../schema/common.json', 'r', encoding='utf-8') as f0:
    # extracted_schema1 = f1.read()
    extracted_schema0 = json.load(f0)
    # print(extracted_schema1)

with open('../../schema/finbench.json', 'r', encoding='utf-8') as f1:
    # extracted_schema1 = f1.read()
    extracted_schema1 = json.load(f1)
    # print(extracted_schema1)

with open('../../schema/movie.json', 'r', encoding='utf-8') as f2:
    extracted_schema2 = json.load(f2)

with open('../../schema/the_three_body.json', 'r', encoding='utf-8') as f3:
    extracted_schema3 = json.load(f3)

with open('../../schema/yago.json', 'r', encoding='utf-8') as f4:
    extracted_schema4 = json.load(f4)

with open('step5_question2cypher_prompt.txt', 'r', encoding='utf-8') as f5:
    prompt = f5.read()


import os

# 文件夹路径
folder_path = './gen_questions/yago_new_schema/1'
output_folder = './gen_cyphers/yago_new_schema/1'

with tqdm(total=len(os.listdir(folder_path))) as pbar:
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 获取文件名（去掉扩展名）
        basename = os.path.splitext(filename)[0]

        # 分割文件名
        params = basename.split('_')
        # 获取最后三个参数
        db_name = params[-1]
        if db_name == "body":
            num = params[-5]
            hard = params[-4]
            db_name = "the_three_body"
        else:
            num = params[-3]
            hard = params[-2]

        if db_name == "finbench":
            schema = extracted_schema1
        elif db_name == "movie":
            schema = extracted_schema2
        elif db_name == "the_three_body":
            schema = extracted_schema3
        elif db_name == "yago":
            schema = extracted_schema4
        elif db_name == "common":
            schema = extracted_schema0

        file_path = os.path.join(folder_path, filename)
        output_file_path = f"{output_folder}/step5_question2cypher_res_{num}_{hard}_{db_name}.txt"

        # 检查输出文件是否已存在，如果存在则跳过
        if os.path.exists(output_file_path):
            print(f"File {output_file_path} already exists. Skipping...")
            pbar.update(1)
            continue

        # 确保文件是一个普通文件而不是目录
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取文件内容
                question = file.read()

        cur_prompt = prompt.replace('{schema}', str(schema)).replace('{question}', question)

        output = call_gpt4o(cur_prompt)

        # Print the outputs.
        with open(output_file_path, "w",encoding="utf-8") as f7:
            f7.write(output)
            # print(len(encoding.encode(output)))
            # 更新进度条
            pbar.update(1)

print(f"Processing completed.")


