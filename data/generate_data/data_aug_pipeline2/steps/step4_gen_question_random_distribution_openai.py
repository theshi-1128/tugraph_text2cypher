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
                max_tokens=1000,  # 设置最大返回 token 数量
                n=1,  # 生成一个响应
                stop=None,  # 设置停止条件
                temperature=0.7  # 调整生成文本的多样性
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(f"Error: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # 如果出错则等待10秒后重试


with open('../../schema/yago.json','r',encoding='utf-8') as f0:
    extracted_schema0 = f0.read()

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
extracted_schema = [extracted_schema0]

with open('step4_gen_real_question_random_prompt.txt', 'r', encoding='utf-8') as f5:
    prompt = f5.read()

with tqdm(total = 1500) as pbar:
    for id, schema in enumerate(extracted_schema):
        if id == 0:
            name = "yago"
        # elif id == 1:
        #     name = "yago"
        # elif id == 2:
        #     name = "finbech"
        # elif id == 3:
        #     name = "movie"
        # elif id == 4:
        #     name = "the_three_body"

        rules = []
        with open(f'./extract_question_dir/merged_{name}_dir.txt', 'r', encoding='utf-8') as f6:
            tricks = f6.readlines()
            for rule in tricks:
                rules.append(rule)

        l = len(rules)

        for hard in range(1, 4):
            for j in range(500):
                chosen_rules = []
                random.seed()
                choice = random.sample(range(0, l), hard)
                for i in choice:
                    chosen_rules.append(rules[i])

                cur_prompt = prompt.replace('{schema}', schema).replace('{rules}', str(chosen_rules))

                output = call_gpt4o(cur_prompt)

                # print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
                with open(f"gen_questions/yago_new_schema/{hard}/step4_gen_questions_random_distribution_res_{j}_{hard}_{name}.txt",
                          "w", encoding="utf-8") as f7:
                    f7.write(output)
                    pbar.update(1)


