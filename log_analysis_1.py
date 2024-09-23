import json
import pandas as pd

# 設定檔案路徑
log_file_path = "D:\\Harry\\Feature matching\\Moto_Bluecat\\feature_matching_tool\\debug\\20240825_roi\\save.log"  # 替換為你的 log 檔路徑
csv_file_path = "D:\\Harry\\Feature matching\\Moto_Bluecat\\20240825\\20240825.csv"  # 替換為你的 CSV 檔路徑（可選）
output_log_path = "D:\\Harry\\Feature matching\\Moto_Bluecat\\20240825\\output_log_roi.txt"  # 替換為輸出的 log 檔路徑

""" 檢查 matching points threshold 工具 """


# 讀取 log 檔
with open(log_file_path, 'r', encoding='utf-8') as log_file:
    log_data = json.load(log_file)

# 初始化統計變數
total = 0
correct = 0
failed_30 = 0
failed_level = 0

# 初始化名單變數
failed_30_list = []
correct_list = []
failed_level_list = []

# 定義輸出清單的函數來簡化重複程式
def output_list(output_file, list_name, data_list):
    output_file.write(f"\n{list_name}:\n")  # 在每個清單前空一行
    for item in data_list:
        output_file.write(f"Name: {item['name']}, First MP: {item['First MP']}, Second MP: {item['Second MP']}, First Match: {item['First Match']}, Second Match: {item['Second Match']}\n")

# 移除前綴 "roi_" 的函數
def remove_roi_prefix(filename):
    if filename.startswith("roi_"):
        return filename.replace("roi_", "")
    return filename

# 檢查 log 檔中的每一筆資料
for roi_key, roi_value in log_data.items():
    roi_key_clean = remove_roi_prefix(roi_key)
    
    if not roi_key_clean.startswith("2-"):
        continue

    total += 1  # 每檢查一筆資料，total +1

    pool = roi_value.get("pool", {})
    if not pool:
        continue

    # 根據 matching_points 對 "1-" 資料進行排序
    sorted_pool = sorted(pool.items(), key=lambda item: item[1]["matching_points"], reverse=True)
    
    first_match_name = sorted_pool[0][0]  # 第一名的檔案名稱
    first_match_points = sorted_pool[0][1]["matching_points"]
    second_match_name = sorted_pool[1][0] if len(sorted_pool) > 1 else "N/A"
    second_match_points = sorted_pool[1][1]["matching_points"] if len(sorted_pool) > 1 else "N/A"

    # Step 4: 進行 M.P. 檢查
    if first_match_points < 30:
        failed_30_list.append({
            "name": roi_key,  # 保留原始名稱
            "First MP": first_match_points,
            "Second MP": second_match_points,
            "First Match": first_match_name,
            "Second Match": second_match_name
        })
        failed_30 += 1
        continue

    # Step 5: 檢查 M.P. 差距
    if first_match_points - second_match_points >= 20:
        correct_list.append({
            "name": roi_key,  # 保留原始名稱
            "First MP": first_match_points,
            "Second MP": second_match_points,
            "First Match": first_match_name,
            "Second Match": second_match_name
        })
        correct += 1
    else:
        failed_level_list.append({
            "name": roi_key,  # 保留原始名稱
            "First MP": first_match_points,
            "Second MP": second_match_points,
            "First Match": first_match_name,
            "Second Match": second_match_name
        })
        failed_level += 1

# 計算正確率
accuracy = (correct / total) * 100 if total > 0 else 0

# 輸出結果到 log 檔
with open(output_log_path, 'w', encoding='utf-8') as output_file:
    # 輸出統計結果
    output_file.write(f"Total checked: {total}\n")
    output_file.write(f"Correct matches: {correct}\n")
    output_file.write(f"Accuracy: {accuracy:.2f}%\n")  # 顯示正確率
    output_file.write(f"Failed_30: {failed_30}\n")
    output_file.write(f"Failed_level: {failed_level}\n")

    # 使用函數來輸出清單，並按順序：failed_30_list, failed_level_list, correct_list
    output_list(output_file, "failed_30_list", failed_30_list)
    output_list(output_file, "failed_level_list", failed_level_list)
    output_list(output_file, "correct_list", correct_list)
