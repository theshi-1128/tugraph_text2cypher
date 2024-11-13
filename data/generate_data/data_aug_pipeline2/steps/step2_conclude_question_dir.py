import json
import openai
import time
from tqdm import tqdm
import os


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


with open('step2_conclude_question_dir_prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read()

path = './extract_question_dir/common'
num = sum([len(files) for _, _, files in os.walk(path)])

with tqdm(total=num) as pbar:
    i = 0
    while i < num:
        with open(f"extract_question_dir/common/step1_extract_dir_train_data_res_{i}.txt",'r',encoding='utf-8') as f1:
            data = f1.read()
        i += 1

        cur_prompt = prompt.replace('{question_dir}', data)

        output = call_gpt4o(cur_prompt)

        with open(f"conclude_question_dir/common/step2_conclude_question_dir_res_{i}.txt", "w", encoding="utf-8") as f3:
            f3.write(output)
            pbar.update(1)



