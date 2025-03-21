import numpy as np
import rootutils
rootutils.setup_root(__file__,
                     indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
                     pythonpath=True)
from core.data.extract_feature import extract_sunset_features
from core.utils.write_read import load_json

def distance(vec1, vec2):
    dist = np.linalg.norm(np.array(vec1) - np.array(vec2))
    return dist.item()

def feature_fusion(feature_image):
    features = []
    for key, value in feature_image.items():
        if key != "image_name":
            features.extend(value)
    return features

def similar_most_image(src_image, path_dataset_image, num):
    features = extract_sunset_features(src_image)
    dataset_image = load_json(path_dataset_image)
    name_score = [
        (item["image_name"], distance(feature_fusion(features), feature_fusion(item)))
        for item in dataset_image
    ]
    name_score.sort(key=lambda x : x[1])
    print_image_similar(name_score[:num])

def print_image_similar(name_score):
    print("Image the most similar:")
    for name, score in name_score:
        print(f"Image: {name} - Score: {score}")
    print("-----------------------")
    
if __name__ == "__main__":
    path_image = "images_csdldpt/AKVED48oXJo.jpg"
    path_dataset = "data_storage/json/feature_extract.json"
    num = 20
    similar_most_image(path_image, path_dataset, num)
    
    

    
    