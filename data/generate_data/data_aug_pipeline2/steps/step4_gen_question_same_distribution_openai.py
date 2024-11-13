import json
import openai
import time
from tqdm import tqdm
import os
import random
from openai import OpenAI
from openai import OpenAIError, RateLimitError, APIError, Timeout
client = OpenAI()



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


with open('../../schema/yago.json','r',encoding='utf-8') as f0:
    extracted_schema5 = f0.read()

#
# with open('step1_extract_placeholder_finbench.txt', 'r', encoding='utf-8') as f1:
#     extracted_schema1 = f1.read()
#
# with open('step1_extract_placeholder_movie.txt', 'r', encoding='utf-8') as f2:
#     extracted_schema2 = f2.read()
#
# with open('step1_extract_placeholder_the_three_body.txt', 'r', encoding='utf-8') as f3:
#     extracted_schema3 = f3.read()
#
# with open('step1_extract_placeholder_yago.txt', 'r', encoding='utf-8') as f4:
#     extracted_schema4 = f4.read()

# extracted_schema = [extracted_schema1, extracted_schema2, extracted_schema3, extracted_schema4]

with open('step4_gen_real_question_prompt.txt', 'r', encoding='utf-8') as f5:
    prompt = f5.read()

rules = []
# with open('./conclude_rules/merged_common_rules.txt', 'r', encoding='utf-8') as f6:
#     tricks = f6.readlines()
#     for rule in tricks:
#         rules.append(rule)

# for id, schema in enumerate(extracted_schema5):
name = "yago"
# if id == 0:
#     name = "finbench"
# elif id == 1:
#     name = "movie"
# elif id == 2:
#     name = "the_three_body"
# elif id == 3:
#     name = "yago"
with open("../../given_data/train_yago_data.json", 'r', encoding='utf-8') as f7:
    train_examples = json.load(f7)

with open("../../given_data/test_yago_data.json", 'r', encoding='utf-8') as f8:
    test_examples = json.load(f8)

# 要搜索的根目录
folder_path = "./extract_question_dir/yago"

with tqdm(total=len(os.listdir(folder_path))) as pbar:
    index = 0
    for filename in os.listdir(folder_path):
        # 获取每个文件的完整路径
        file_path = os.path.join(folder_path, filename)
        basename = os.path.splitext(filename)[0]
        # 分割文件名
        params = basename.split('_')
        # 获取最后三个参数
        num = params[-1]
        # print(num)
        # if "train" in filename:
        #     with open(file_path, 'r', encoding='utf-8') as f6:
        #         tricks = f6.read()
        #         # print(tricks)
        #
        #     example = ""
        #     for i, data in enumerate(train_examples):
        #         if i != int(num):
        #             continue
        #         example = str(data)
        #         break
            # print(example)

        if "test" in filename:
            with open(file_path, 'r', encoding='utf-8') as f6:
                tricks = f6.read()
                # print(tricks)

            example = ""
            for i, data in enumerate(test_examples):
                if i != int(num):
                    continue
                example = str(data)
                break
            # print(example)

            cur_prompt = prompt.replace('{schema}', extracted_schema5).replace('{rules}', tricks).replace('{data}',example)

            output = call_gpt4o(cur_prompt)

            # Print the outputs.
            with open(f"gen_questions/yago_new_schema/same_distribution_as_dataset/step4_gen_questions_test_res_{index}_{name}.txt",
                      "w", encoding="utf-8") as f9:
                f9.write(output)
                pbar.update(1)
                index += 1

#
# with tqdm(total=1200) as pbar:
#
#     for hard in range(1, 2):
#         for j in range(600-179):
#             temp = j + 179
#             chosen_rules = []
#             random.seed()
#             choice = random.sample(range(0, l), hard)
#             for i in choice:
#                 chosen_rules.append(rules[i])
#
#             cur_prompt = prompt.replace('{schema}', extracted_schema5).replace('{rules}', str(chosen_rules))
#
#             output = call_gpt4o(cur_prompt)
#
#             # Print the outputs.
#             with open(f"gen_questions/common/step4_gen_questions_res_{temp}_{hard}_{name}.txt",
#                       "w", encoding="utf-8") as f8:
#                 f7.write(output)
#                 pbar.update(1)


