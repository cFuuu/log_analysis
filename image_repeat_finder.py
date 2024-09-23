import os
import shutil
import pandas as pd

# 讀取 Excel 檔案
excel_file = "D:\\Harry\\Feature matching\\Moto_Bluecat\\20240825\\repeat.xlsx"  # 你的 Excel 檔案名稱
df = pd.read_excel(excel_file)  # 讀取 Excel 資料
source_folder = "D:\\Harry\\Feature matching\\Moto_Bluecat\\Parking_data\exit_data\\20240825_out"  # 圖片所在的資料夾
output_folder = "D:\\Harry\\Feature matching\\\\Moto_Bluecat\\20240825\\0825_exit_2"  # 複製後的目標資料夾

""" 
檢查excel兩個欄位("plate", "dasequencemun")，找出欄位的("plate")的檔案，將照片複製到新的資料夾，
若"plate"有出現重複，則直接跳過複製

"""


# 確認目標資料夾存在，若不存在則創建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 用於追蹤已處理的 plate
seen_plates = set()

# 遍歷 Excel 檔案中的每一行
for index, row in df.iterrows():
    plate = row['plate']  # 車牌。"Excel欄位名稱"
    image_name = row['dasequencenum']  # 圖檔名稱。"Excel欄位名稱" 

    # 檢查車牌是否已處理過
    if plate not in seen_plates:
        seen_plates.add(plate)  # 記錄此車牌

        # 遍歷資料夾內的所有檔案，忽略副檔名進行比對
        for file_name in os.listdir(source_folder):
            # 去除資料夾內檔案的副檔名，僅保留檔名
            base_name = os.path.splitext(file_name)[0]

            # 如果 Excel 中的檔名與資料夾內檔名相同（忽略副檔名）
            if base_name == image_name:
                source_file = os.path.join(source_folder, file_name)
                
                # 檢查檔案是否存在，若存在則進行複製
                if os.path.exists(source_file):
                    shutil.copy(source_file, output_folder)  # 複製檔案
                    print(f'複製成功: {file_name}')
                else:
                    print(f'檔案未找到: {file_name}')
                break  # 一旦找到檔案就停止搜尋
    else:
        print(f'跳過重複車牌: {plate}')
