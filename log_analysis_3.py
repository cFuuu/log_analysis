import json
import pandas as pd

# 設定檔案路徑
log_file_path = "D:\\Harry\\Feature matching\\Moto_Bluecat\\feature_matching_tool\\debug\\20240825_roi\\save.log"  # 替換為你的 log 檔路徑
csv_file_path = "D:\\Harry\\Feature matching\\Moto_Bluecat\\20240825\\20240825.csv"  # 替換為你的 CSV 檔路徑（可選）
output_log_path = "D:\\Harry\\Feature matching\\Moto_Bluecat\\20240825\\output_log_roi.txt"  # 替換為輸出的 log 檔路徑

""" 檢查 matching points threshold tool 
含有LPR檢查功能，可以自行決定啟閉，但經測試還是有問題故不使用。 """



# 控制 LPR 檢查的開關
ENABLE_LPR_CHECK = False

# 讀取 log 檔
with open(log_file_path, 'r', encoding='utf-8') as log_file:
    log_data = json.load(log_file)

# 讀取 CSV 檔（如果有）
excel_data = None
if ENABLE_LPR_CHECK:
    excel_data = pd.read_csv(csv_file_path)

# 初始化統計變數
total = 0
correct = 0
failed_30 = 0
failed_level = 0
failed_LPR = 0

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

# LPR 檢查功能函數
def check_LPR_match(file1, file2, excel_data):
    """
    檢查兩個檔案名在 CSV 檔中的 LPR 車牌號碼是否匹配。
    :param file1: 第一個檔案名稱（可能以 "1-" 開頭）
    :param file2: 第二個檔案名稱（可能以 "1-" 開頭）
    :param excel_data: 讀取的 CSV 資料表（DataFrame）
    :return: 如果 LPR 匹配，返回 True；否則返回 False。
    """
    file1_clean = remove_roi_prefix(file1)  # 去除 "roi_" 進行查找
    file2_clean = remove_roi_prefix(file2)  # 去除 "roi_" 進行查找

    lpr_file1 = excel_data.loc[excel_data['dasequencenum'] == file1_clean, 'plate'].values
    lpr_file2 = excel_data.loc[excel_data['dasequencenum'] == file2_clean, 'plate'].values
    
    if len(lpr_file1) > 0 and len(lpr_file2) > 0:
        return lpr_file1[0] == lpr_file2[0]
    return False

# 繼續檢查 "1-" 名單，直到找到 LPR 不同的兩個檔案
def find_different_LPR(sorted_pool, first_match_name, excel_data):
    first_match_clean = remove_roi_prefix(first_match_name)
    first_match_lpr = excel_data.loc[excel_data['dasequencenum'] == first_match_clean, 'plate'].values
    if len(first_match_lpr) == 0:
        print(f"Warning: No LPR found for first match: {first_match_name}")
        return None, None
    first_match_lpr = first_match_lpr[0]
    
    # 循環檢查 "1-" 檔案，直到找到不同的 LPR
    for index, (match_name, data) in enumerate(sorted_pool[1:], start=2):
        match_clean = remove_roi_prefix(match_name)
        match_lpr = excel_data.loc[excel_data['dasequencenum'] == match_clean, 'plate'].values
        if len(match_lpr) == 0:
            print(f"Warning: No LPR found for match: {match_name}")
            continue  # 跳過這個沒有 LPR 的資料
        
        match_lpr = match_lpr[0]
        if first_match_lpr != match_lpr:
            # 找到兩個不同的 LPR，打印結果
            print(f"LPR mismatch found:")
            print(f"First LPR: {first_match_name}, LPR: {first_match_lpr}")
            print(f"Second LPR: {match_name}, LPR: {match_lpr}")
            return first_match_name, match_name  # 返回兩個不同 LPR 的檔案
    
    return None, None  # 如果沒有找到不同的 LPR


# 檢查 log 檔中的每一筆資料
for roi_key, roi_value in log_data.items():
    roi_key_clean = remove_roi_prefix(roi_key)
    
    if not roi_key_clean.startswith("2-"):
        continue

    total += 1  # 每檢查一筆資料，total +1

    pool = roi_value.get("pool", {})
    if not pool:
        continue

    sorted_pool = sorted(pool.items(), key=lambda item: item[1]["matching_points"], reverse=True)
    
    first_match_name = sorted_pool[0][0]  # 第一名的檔案名稱

    # Step 2: LPR 檢查，尋找不同 LPR 的兩個 "1-" 檔案
    if ENABLE_LPR_CHECK and excel_data is not None:
        different_1, different_2 = find_different_LPR(sorted_pool, first_match_name, excel_data)
        if different_1 is None or different_2 is None:
            failed_LPR += 1
            continue  # 如果沒有找到不同的 LPR，則跳過該條目

    # Step 4: 進行 M.P. 檢查
    first_match_points = sorted_pool[0][1]["matching_points"]
    second_match_points = sorted_pool[1][1]["matching_points"] if len(sorted_pool) > 1 else "N/A"

    if first_match_points < 30:
        failed_30_list.append({
            "name": roi_key,  # 保留原始名稱
            "First MP": first_match_points,
            "Second MP": second_match_points,
            "First Match": first_match_name,
            "Second Match": sorted_pool[1][0] if len(sorted_pool) > 1 else "N/A"
        })
        failed_30 += 1
        continue

    if first_match_points - second_match_points >= 20:
        correct_list.append({
            "name": roi_key,  # 保留原始名稱
            "First MP": first_match_points,
            "Second MP": second_match_points,
            "First Match": first_match_name,
            "Second Match": sorted_pool[1][0] if len(sorted_pool) > 1 else "N/A"
        })
        correct += 1
    else:
        failed_level_list.append({
            "name": roi_key,  # 保留原始名稱
            "First MP": first_match_points,
            "Second MP": second_match_points,
            "First Match": first_match_name,
            "Second Match": sorted_pool[1][0] if len(sorted_pool) > 1 else "N/A"
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
    output_file.write(f"Failed_LPR matches: {failed_LPR}\n")
    output_file.write(f"Failed_30: {failed_30}\n")
    output_file.write(f"Failed_level: {failed_level}\n")

    # 使用函數來輸出清單，並按順序：failed_30_list, failed_level_list, correct_list
    output_list(output_file, "failed_30_list", failed_30_list)
    output_list(output_file, "failed_level_list", failed_level_list)
    output_list(output_file, "correct_list", correct_list)
