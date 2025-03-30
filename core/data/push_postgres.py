import psycopg2
import json
import os

# 1. Load JSON Data
with open(r"D:\work\IDE\PyCharm\Project\Image_Retrieval_System\data_storage\json\feature_extract.json", "r") as f:
    features_list = json.load(f)

# 2. Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Ditm3may!",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# 3. Iterate over JSON entries
for entry in features_list:
    # Read image binary data
    image_path = os.path.join("D:\work\IDE\PyCharm\Project\Image_Retrieval_System\images_csdldpt", entry["image_name"])
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Insert into database
    cursor.execute("""
        INSERT INTO image_features (
            image_name, dominant_color, contrast, 
            sun_position, light_blur, light_reflection, horizon_line, 
            cloud_density, image_composition, overall_brightness, auxiliary_elements
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        entry["image_name"],
        entry["Dominant_Color"],
        entry["Contrast"],
        entry["Sun_Position"],
        entry["Light_Blur"],
        entry["Light_Reflection"],
        entry["Horizon_Line"],
        entry["Cloud_Density"],
        entry["Image_Composition"],
        entry["Overall_Brightness"],
        entry["Auxiliary_Elements"]
    ))

conn.commit()
cursor.close()
conn.close()