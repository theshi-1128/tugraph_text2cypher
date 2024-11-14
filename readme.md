# 2024 CCF BDCI 

赛题2 「AI for TuGraph」小样本条件下的自然语言至图查询语言翻译大模型微调 A榜12名思路分享

If you find this work useful in your own research, please feel free to leave a star⭐️!


## 细节：

- 微调模型qwen2.5-14b-instruct
- 第一阶段训练数据构造方法：从200条训练数据总结构造规则，随机组合，结合schema生成训练数据
- 第二阶段数据构造：从训练集测试集给定的自然语言问题，总结带占位符的模板问题，结合schema生成训练数据
- 生成训练数据采用openai gpt4o api接口
- 微调脚本run_all.sh：两阶段微调
- 对不同schema训练不同模型，lora
- 一阶段数据量：5k，二阶段数据量1k
