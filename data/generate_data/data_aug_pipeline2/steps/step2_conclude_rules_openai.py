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


with open('step2_conclude_rules_prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read()

path = './conclude_train_data/common'
num = sum([len(files) for _, _, files in os.walk(path)])

with tqdm(total=num) as pbar:
    i = 0
    while i < num:
        with open(f"conclude_train_data/common/step1_conclude_train_data_res_{i}.txt",'r',encoding='utf-8') as f1:
            data_1 = f1.read()
        if i+1 >= num:
            data_2 = " "
        else:
            with open(f"conclude_train_data/common/step1_conclude_train_data_res_{i+1}.txt",'r',encoding='utf-8') as f2:
                data_2 = f2.read()
        if i+2 >= num:
            data_3 = " "
        else:
            with open(f"conclude_train_data/common/step1_conclude_train_data_res_{i+2}.txt",'r',encoding='utf-8') as f3:
                data_3 = f3.read()
        if i+3 >= num:
            data_4 = " "
        else:
            with open(f"conclude_train_data/common/step1_conclude_train_data_res_{i+3}.txt",'r',encoding='utf-8') as f4:
                data_4 = f4.read()
        if i+4 >= num:
            data_5 = " "
        else:
            with open(f"conclude_train_data/common/step1_conclude_train_data_res_{i+4}.txt",'r',encoding='utf-8') as f5:
                data_5 = f5.read()
        i += 5

        cur_prompt = prompt.replace('{first_conclude}', data_1).replace('{second_conclude}', data_2).replace('{third_conclude}', data_3).replace('{fourth_conclude}', data_4).replace('{fifth_conclude}', data_5)

        output = call_gpt4o(cur_prompt)

        with open(f"conclude_rules/common/step2_conclude_rules_res_{i//5}.txt", "w", encoding="utf-8") as f3:
            f3.write(output)
            pbar.update(5)



