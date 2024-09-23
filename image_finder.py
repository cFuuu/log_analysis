import os
import shutil
import pandas as pd

""" 查詢Excel欄位, 含有其"圖檔檔名"的圖檔複製到新的資料夾 """

# 讀取 Excel 檔
excel_file = "D:\\Harry\\Feature matching\\Car_XuYi\\20240615\\match_result.xlsx"  # Excel 檔名
df = pd.read_excel(excel_file)  # 讀取 Excel 檔
file_names = df["2nd_match_result"].tolist()  # 假設檔案名在 "檔案名" 這一列

# 圖檔所在的資料夾
source_folder = 'D:\\Harry\\Feature matching\\Car_XuYi\\feature_matching_tool\\debug\\20240615_roi' 
# 複製後的資料夾
output_folder = 'D:\\Harry\\Feature matching\\Car_XuYi\\20240615\\2nd_match_result'  

# 確認目標資料夾存在，若不存在則創建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍歷資料夾中的所有檔案
for file_name in os.listdir(source_folder):
    # 去除資料夾內檔案的副檔名，僅保留檔名
    base_name = os.path.splitext(file_name)[0]

    # 檢查 Excel 檔案列表中的名稱，並忽略副檔名
    if base_name in file_names:
        source_file = os.path.join(source_folder, file_name)
        shutil.copy(source_file, output_folder)  # 複製檔案
        print(f'複製成功: {file_name}')
    else:
        print(f'未找到對應檔案: {file_name}')
