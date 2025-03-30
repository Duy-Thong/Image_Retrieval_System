import json
from pathlib import Path
import cv2
import numpy as np
import glob
from multiprocessing import Pool, cpu_count
from PIL import Image

def get_files_in_folder(path_folder):
    file_paths = glob.glob(f"{path_folder}/*.jpg")
    return file_paths
    
def extract_sunset_features(image_path):
    # Read the image from the path
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 533))
    
    if image is None:
        raise ValueError("Unable to read the image from the provided path.")
    
    # Convert the image to RGB (OpenCV defaults to BGR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    
    # Calculate the features
    features = {}
    features["image_name"] = Path(image_path).name
    
    # 1. Dominant color (average color)
    avg_color = np.mean(image_rgb, axis=(0, 1))
    features["Dominant_Color"] = avg_color.tolist()
    
    # 2. Contrast
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contrast = gray_image.std()
    features["Contrast"] = [float(contrast)]
    
    # 3. Sun position (assume the sun is the brightest spot)
    bright_spot = np.unravel_index(np.argmax(gray_image), gray_image.shape)
    features["Sun_Position"] = [int(bright_spot[0]), int(bright_spot[1])]
    
    # 4. Light blur (using the standard deviation of brightness)
    brightness_std = gray_image.std()
    features["Light_Blur"] = [float(brightness_std)]
    
    # 5. Light reflection (assume reflection is the bright areas near the horizon)
    height, width, _ = image.shape
    horizon_region = image_rgb[int(height * 0.7):, :]
    reflection_intensity = np.mean(horizon_region)
    features["Light_Reflection"] = [float(reflection_intensity)]
    
    # 6. Horizon line (assume the horizon is at 2/3 of the image height)
    features["Horizon_Line"] = [int(height * 0.66)]
    
    # 7. Clouds (analyze areas with high contrast)
    edges = cv2.Canny(gray_image, 100, 200)
    cloud_density = np.sum(edges) / (height * width)
    features["Cloud_Density"] = [float(cloud_density)]
    
    # 8. Image composition (rule of thirds)
    rule_of_thirds = {
        "top_left": image_rgb[:height//3, :width//3],
        "top_right": image_rgb[:height//3, 2*width//3:],
        "bottom_left": image_rgb[2*height//3:, :width//3],
        "bottom_right": image_rgb[2*height//3:, 2*width//3:]
    }
    features["Image_Composition"] = [float(np.mean(v)) for k, v in rule_of_thirds.items()]
    
    # 9. Overall brightness
    brightness = np.mean(gray_image)
    features["Overall_Brightness"] = [float(brightness)]
    
    # 10. Auxiliary elements (edge detection to identify objects)
    edges = cv2.Canny(gray_image, 100, 200)
    object_density = np.sum(edges) / (height * width)
    features["Auxiliary_Elements"] = [float(object_density)]    
    
    return features

def multiprocess(paths):
    with Pool(processes=cpu_count() - 1) as pool:
        ls_features = pool.map(extract_sunset_features, paths)
        pool.close()
    return ls_features

def save_feature(data, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print("Write successful") 

if __name__ == "__main__":
    path_folder = "/home/vutuyen/Documents/W_SUZERAIN_W5/Project/Image_Retrieval_System/images_csdldpt"
    path_save = "/home/vutuyen/Documents/W_SUZERAIN_W5/Project/Image_Retrieval_System/data_storage/json/feature_extract_800_533.json"
    length = 295
    paths = get_files_in_folder(path_folder=path_folder)[:length]
    ls_features = multiprocess(paths=paths)
    save_feature(ls_features, path_save)
    
