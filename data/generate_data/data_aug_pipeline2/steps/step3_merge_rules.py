import os

# 文件夹路径
folder_path = './extract_question_dir/yago'
output_file = 'extract_question_dir/merged_yago_dir.txt'

# 打开输出文件
with open(output_file, 'w', encoding='utf-8') as output:
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            if "test" in filename:
                file_path = os.path.join(folder_path, filename)
                # 确保文件是一个普通文件而不是目录
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # 读取文件内容
                        lines = file.readlines()
                        # print(filename)
                        # 遍历每一行，提取 "1. content" 或 "2. content" 的内容
                        for line in lines:
                            content = line.split(". ", 1)[1].strip()  # 去掉 "1. " 或 "2. " 并提取后面的内容
                            output.write(content + '\n')  # 将内容写入输出文件中，每行一条