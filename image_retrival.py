from core.data.extract_feature import extract_sunset_features
import numpy as np
from scipy.spatial.distance import euclidean
import json

def find_similar_images(query_features, image_db, top_n=5):
    distances = []

    for data in image_db:
        feature_vector = (
                data["Dominant_Color"] +
                data["Contrast"] +
                data["Sun_Position"] +
                data["Light_Blur"] +
                data["Light_Reflection"] +
                data["Horizon_Line"] +
                data["Cloud_Density"] +
                data["Image_Composition"] +
                data["Overall_Brightness"] +
                data["Auxiliary_Elements"]
        )
        query_vector = (
                query_features["Dominant_Color"] +
                query_features["Contrast"] +
                query_features["Sun_Position"] +
                query_features["Light_Blur"] +
                query_features["Light_Reflection"] +
                query_features["Horizon_Line"] +
                query_features["Cloud_Density"] +
                query_features["Image_Composition"] +
                query_features["Overall_Brightness"] +
                query_features["Auxiliary_Elements"]
        )

        dist = euclidean(feature_vector, query_vector)
        distances.append((data["image_name"], dist))

    # Sort images by ascending distance (smaller distance = more similar)
    distances.sort(key=lambda x: x[1])

    return distances[:top_n]



if __name__ == "__main__":
    features = extract_sunset_features("test_img.jpg")
    with open(r"D:\work\IDE\PyCharm\Project\Image_Retrieval_System\data_storage\json\feature_extract.json") as json_file:
        data = json.load(json_file)
        # Find top 3 similar images
        top_matches = find_similar_images(features, data, top_n=3)
        # Output results
        for rank, (image_name, similarity) in enumerate(top_matches, 1):
            print(f"{rank}. {image_name} (Distance: {similarity:.4f})")