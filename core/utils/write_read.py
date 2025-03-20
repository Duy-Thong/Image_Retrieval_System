import json


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

data = load_json("/home/vutuyen/Documents/W_SUZERAIN_W5/Project/Image_Retrieval_System/data_storage/json/feature_extract.json")
print(data[0])