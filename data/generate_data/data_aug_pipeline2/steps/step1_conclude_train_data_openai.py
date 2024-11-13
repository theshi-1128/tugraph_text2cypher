import json
import openai
import time
from tqdm import tqdm


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
            response = openai.ChatCompletion.create(
                model="gpt-4o-2024-08-06",  # 指定模型名称
                messages=messages,
                max_tokens=1000,  # 设置最大返回 token 数量
                n=1,  # 生成一个响应
                stop=None,  # 设置停止条件
                temperature=0.7  # 调整生成文本的多样性
            )
            return response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            print(f"Error: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # 如果出错则等待10秒后重试


with open('../../test_common_data.json', 'r', encoding='utf-8') as f1:
    data = json.load(f1)
    # single_data = data[0]

with open('step1_extract_question_directions_prompt.txt','r',encoding='utf-8') as f2:
    prompt = f2.read()


import os


with tqdm(total=len(data)) as pbar:
    for i, item in enumerate(data):
        cur_prompt = prompt.replace('{single_train_data}', str(item))

        output = call_gpt4o(cur_prompt)

        with open(f"extract_question_dir/common/step1_extract_dir_test_data_res_{i}.txt", "w", encoding="utf-8") as f3:
            f3.write(output)
            pbar.update(1)



