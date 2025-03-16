# Description: Lọc dữ liệu trong file Excel dựa trên danh sách file ảnh trong thư mục, loại bỏ các dòng không có ảnh tương ứng, đảm bảo dữ liệu trong file Excel luôn đồng bộ với ảnh trong thư mục.
import os
import pandas as pd

# Thư mục chứa ảnh
image_folder = "D:\Learning\CSDLDPT\images_csdldpt"

# File Excel
excel_file = "D:\Learning\CSDLDPT\Image Data.xlsx"
sheet_name = "Sunset"  # Thay đổi nếu sheet có tên khác

# Lấy danh sách các file trong thư mục
image_files = {os.path.splitext(f)[0] for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))}

# Đọc file Excel
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Giả sử cột chứa ID là 'ID', lọc giữ lại các dòng có ID trùng với danh sách file ảnh
df_filtered = df[df['id'].astype(str).isin(image_files)]

# Ghi lại vào file Excel (ghi đè)
with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
    df_filtered.to_excel(writer, sheet_name=sheet_name, index=False)

print("Done!")
