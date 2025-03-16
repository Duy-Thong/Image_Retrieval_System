import requests
import pandas as pd
import time

ACCESS_KEYS = [
    "dBZizpCXDxyux6XI_xL77gTGYRbK0KYXNhyERa6irKw",
    "VVdRqjUIgLgumyc7FC5pkf6I8zY0hQ-R-AoioSfocHU",
    "nUiDQEA9wKQgmUSORc-cm-f7DDvT0GbjIyJXoExLhr0",
    "GzeDN7YGzAKwPzYWYUOe2Ycanxzal3aavUyXnYQXqeE",
    "skNrwPvZmLPkvSyVuldCDPAZeBFJ4dJg1Bw12ButExk",
    "NCoeGxpLMUX2AGqsAwj_uC0N_dk2QqDPzftCNS5uEVg",
]

URL = "https://api.unsplash.com/search/photos"

QUERY_LIMIT = 50
global_page = 1

all_images = []

for access_key in ACCESS_KEYS:
    print(f"🔑 Đang sử dụng API Key: {access_key}")

    for _ in range(QUERY_LIMIT):
        print(f" - Query page {global_page}...")

        params = {
            "query": "sunset-sun",
            "client_id": access_key,
            "per_page": 30,
            "page": global_page,
        }

        response = requests.get(URL, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                results = data.get("results", [])

                for img in results:
                    all_images.append({
                        "id": img["id"],
                        "slug": img["slug"],
                        "created_at": img["created_at"],
                        "updated_at": img["updated_at"],
                        "promoted_at": img["promoted_at"],
                        "width": img["width"],
                        "height": img["height"],
                        "description": img["alt_description"],
                        "links": img["links"]["download"]
                    })

            except requests.exceptions.JSONDecodeError:
                print(f"⚠️ Lỗi JSONDecodeError ở page {global_page}, API Key {access_key}. Bỏ qua request này.")
                global_page += 1
                continue

        else:
            print(f"⚠️ Lỗi {response.status_code} tại page {global_page} với API Key {access_key}")
            print("Phản hồi từ server:", response.text)

        global_page += 1

        time.sleep(1)

df = pd.DataFrame(all_images)
df.to_csv("unsplash_raw.csv", index=False, encoding="utf-8")
print("✅ Dữ liệu thô đã được lưu vào unsplash_raw.csv")

filtered_df = df[(df["width"] == 6000) & (df["height"] == 4000)]

filtered_df.to_csv("unsplash_filtered.csv", index=False, encoding="utf-8")
print("✅ Dữ liệu đã lọc được lưu vào unsplash_filtered.csv")
