import json

# 請將 file1_path 和 file2_path 替換為你的兩個 JSON 檔案路徑
#file1_path = 'D:\\Harry\\Feature matching\\Moto_Bluecat\\feature_matching_tool\\debug\\20240825_full\\save.log'
#file2_path = 'D:\\Harry\\Feature matching\\Moto_Bluecat\\feature_matching_tool\\debug\\20240825_roi\\save.log'
file1_path = 'D:\\Harry\\Feature matching\\Car_XuYi\\feature_matching_tool\\debug\\20240615_full\\save.log'
file2_path = 'D:\\Harry\\Feature matching\\Car_XuYi\\feature_matching_tool\\debug\\20240615_roi\\save.log'

def calculate_improvement_percentage(old_value, new_value):
    if old_value == 0:
        return None  # 防止除以 0
    improvement = ((new_value - old_value) / old_value) * 100
    return improvement

def sum_total_matching_points_in_file(json_file_path):
    total_matching_points = 0
    
    # 打開並讀取 JSON 檔案
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # 讀取 JSON 檔案
        
        # 遍歷所有的 key，檢查是否以 "2-" 開頭
        for key, value in data.items():
            clean_key = key.lstrip('roi_')  # 移除前綴 "roi_"（如果存在）
            if clean_key.startswith("2-") and 'pool' in value:
                # 找到 pool 中的 "1-" 開頭的 key
                for pool_key, pool_value in value['pool'].items():
                    clean_pool_key = pool_key.lstrip('roi_')  # 移除 pool key 的 "roi_" 前綴
                    if clean_pool_key.startswith("1-") and 'matching_points' in pool_value:
                        total_matching_points += pool_value['matching_points']
    
    return total_matching_points

def compare_total_points(file1_path, file2_path):
    # 讀取兩份檔案中的 matching_points 總數
    file1_total_points = sum_total_matching_points_in_file(file1_path)
    file2_total_points = sum_total_matching_points_in_file(file2_path)
    
    # 計算總數的提升百分比
    improvement = calculate_improvement_percentage(file1_total_points, file2_total_points)
    
    return file1_total_points, file2_total_points, improvement




# 計算總數和提升百分比
file1_total_points, file2_total_points, improvement = compare_total_points(file1_path, file2_path)

# 印出結果
print(f'第一份檔案的 matching_points 總數: {file1_total_points}')
print(f'第二份檔案的 matching_points 總數: {file2_total_points}')
if improvement is not None:
    print(f'總數提升的百分比為: {improvement:.2f}%')
else:
    print('無法計算提升百分比，因為第一份檔案的總數為 0')

