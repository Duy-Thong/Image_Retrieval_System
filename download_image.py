import requests
import os
import pandas as pd

ACCESS_KEY = "NCoeGxpLMUX2AGqsAwj_uC0N_dk2QqDPzftCNS5uEVg"

csv_file = "/kaggle/input/imagedata/Image Data - Sunset (1).csv"
df = pd.read_csv(csv_file)

id_column = "id"
save_folder = "images_csdldpt"

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

def download_unsplash_image(image_id):
    url = f"https://api.unsplash.com/photos/{image_id}/download?client_id={ACCESS_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        download_url = response.json().get("url")

        if download_url:
            image_data = requests.get(download_url).content
            save_path = os.path.join(save_folder, f"{image_id}.jpg")
            with open(save_path, "wb") as file:
                file.write(image_data)

    except requests.exceptions.RequestException:
        pass

df_subset = df.iloc[400:450]

for _, row in df_subset.iterrows():
    image_id = row[id_column]
    if pd.notna(image_id):
        download_unsplash_image(image_id)
