import json

def sum_total_matching_time(json_file_path):
    total_sum = 0
    
    # 打開並讀取 JSON 檔案
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # 讀取 JSON 檔案
        
        # 遍歷所有的 key，忽略前綴 "roi"，並檢查是否以 "2-" 開頭
        for key, value in data.items():
            clean_key = key.lstrip('roi_')  # 移除前面的 "roi"（如果存在）
            if clean_key.startswith("2-") and 'total_matching_time' in value:
                total_sum += value['total_matching_time']
    
    return total_sum

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    return f'{hours} 小時, {minutes} 分鐘, {remaining_seconds} 秒'

def calculate_average_time(total_seconds, data_count):
    if data_count > 0:
        average_time = total_seconds / data_count
        return average_time
    else:
        return 0

# 請將 json_file_path 替換為你的 JSON 檔案路徑
json_file_path = "D:\\Harry\\Feature matching\\Moto_Bluecat\\feature_matching_tool\\debug\\20240825_roi\\save.log"
total_seconds = sum_total_matching_time(json_file_path)

# 讓使用者輸入資料數目
data_count = int(input("請輸入資料數目: "))

# 計算每一筆資料的平均運算時間
average_time = calculate_average_time(total_seconds, data_count)

# 印出總秒數
print(f'Total sum of total_matching_time for "2-" files: {total_seconds} 秒')

# 印出格式化後的總時間
formatted_time = format_time(total_seconds)
print(f'總時間為: {formatted_time}')

# 印出每筆資料的平均運算時間
print(f'每筆資料的平均運算時間為: {average_time:.2f} 秒')
