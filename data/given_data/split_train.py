import json

with open('test_cypher.json','r',encoding='utf-8') as f:
    train_data = json.load(f)
    common_data = []
    finbench_data = []
    movie_data = []
    the_three_body_data = []
    yago_data = []
    for item in train_data:
        if item["db_id"] == "common":
            common_data.append(item)
        elif item["db_id"] == "movie":
            movie_data.append(item)
        elif item["db_id"] == "yago":
            yago_data.append(item)
        elif item["db_id"] == "finbench":
            finbench_data.append(item)
        elif item["db_id"] == "the_three_body":
            the_three_body_data.append(item)

    with open("test_common_data.json",'w',encoding="utf-8") as f2:
        json.dump(common_data,f2,ensure_ascii=False,indent=4)

    with open("test_movie_data.json",'w',encoding="utf-8") as f3:
        json.dump(movie_data,f3,ensure_ascii=False,indent=4)

    with open("test_yago_data.json",'w',encoding="utf-8") as f4:
        json.dump(yago_data,f4,ensure_ascii=False,indent=4)

    with open("test_finbench_data.json",'w',encoding="utf-8") as f5:
        json.dump(finbench_data,f5,ensure_ascii=False,indent=4)

    with open("test_the_three_body_data.json",'w',encoding="utf-8") as f6:
        json.dump(the_three_body_data,f6,ensure_ascii=False,indent=4)

