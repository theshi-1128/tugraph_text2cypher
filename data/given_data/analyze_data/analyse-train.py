import json
from collections import defaultdict

# 关键字分类
clauses = [
    'CREATE', 'DELETE', 'DETACH', 'EXISTS', 'MATCH', 'MERGE', 'OPTIONAL', 
    'REMOVE', 'RETURN', 'SET', 'UNION', 'UNWIND', 'WITH'
]
subclauses = ['LIMIT', 'ORDER', 'SKIP', 'WHERE']
modifiers = ['ASC', 'ASCENDING', 'BY', 'DESC', 'DESCENDING', 'ON']
expressions = ['ALL', 'CASE', 'ELSE', 'END', 'THEN', 'WHEN']
operators = [
    'AND', 'AS', 'CONTAINS', 'DISTINCT', 'ENDS', 'IN', 'IS', 'NOT', 
    'OR', 'STARTS', 'XOR'
]
literals = ['false', 'null', 'true','NULL','TRUE','FALSE']
reserved = [
    'ADD', 'CONSTRAINT', 'DO', 'DROP', 'FOR', 'MANDATORY', 'OF', 'REQUIRE', 
    'SCALAR', 'UNIQUE'
]
aggregate = ['sum(', 'max(', 'min(', 'count(', 'avg(']
all = clauses + subclauses + modifiers + expressions + operators + literals + reserved + aggregate # 所有关键字

# 定义分类函数
def classify_by_keywords(query,keyword_count):
    keywords_found = {
        'Clauses': [],
        'Subclauses': [],
        'Modifiers': [],
        'Expressions': [],
        'Operators': [],
        'Literals': [],
        'Reserved': [],
        'Aggregate': []
    }
    
    # 按类别检查是否包含关键字
    for word in query.split():
        word_cleaned = word.strip('(),":')
        if word_cleaned in all:
            keyword_count[word_cleaned] += 1
        if word_cleaned in clauses:
            keywords_found['Clauses'].append(word_cleaned)
        elif word_cleaned in subclauses:
            keywords_found['Subclauses'].append(word_cleaned)
        elif word_cleaned in modifiers:
            keywords_found['Modifiers'].append(word_cleaned)
        elif word_cleaned in expressions:
            keywords_found['Expressions'].append(word_cleaned)
        elif word_cleaned in operators:
            keywords_found['Operators'].append(word_cleaned)
        elif word_cleaned in literals:
            keywords_found['Literals'].append(word_cleaned)
        elif word_cleaned in reserved:
            keywords_found['Reserved'].append(word_cleaned)
        elif word_cleaned in aggregate:
            keywords_found['Aggregate'].append(word_cleaned)

    return keywords_found

# 暂存json提取的cypher
queries = []
# 统计关键字出现的次数
keyword_count = defaultdict(int)

# 读取并解析 JSON 数据
with open('train_cypher.json','r',encoding='utf-8') as f:
    train_data = json.load(f)
    for item in train_data:
        cypher = item['output']
        queries.append(cypher)  # 使用 append() 而不是 add()

# 对前 10 个查询进行分类
for query in queries:
    result = classify_by_keywords(query,keyword_count)

    # # 统计 'RETURN' 关键字的出现次数
    # return_count = query.upper().count('RETURN')
    # # 如果 'RETURN' 出现两次或更多次，打印提示
    # if return_count >= 2:
    #     print(f"查询中出现了 {return_count} 次 'RETURN': {query}")

    # # 打印每条查询的关键字
    # print(f"查询: {query}")
    # for category, keywords in result.items():
    #     if keywords:
    #         print(f"{category}: {', '.join(keywords)}")
    # print("\n")    ‘

# 打开文件进行写入
with open('cypher_analysis.txt', 'w', encoding='utf-8') as f:
    # 写入总的 Cypher 查询数量
    f.write(f"Total cypher num: {len(queries)}\n\n")
    
    # 写入每种关键字出现的总次数
    f.write("Keyword counts:\n")
    for category, count in keyword_count.items():
        f.write(f"{category}: {count}\n")
