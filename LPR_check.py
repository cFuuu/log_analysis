import json
import pandas as pd

# 假設已經讀取了 Excel 檔
file1 = "2-20240615131321675"
file2 = "1-20240615125442695"

# 請將此路徑替換為Excel檔的實際路徑
csv_file_path = "D:\\Harry\\Feature matching\\Car_XuYi\\Parking_data\\20240615.csv"
# 讀取 CSV 檔
excel_data = pd.read_csv(csv_file_path)

def check_LPR_match(file1, file2, excel_data):
    """
    檢查兩個檔案名在 Excel 檔中的 LPR 車牌號碼是否匹配。
    
    :param file1: 第一個檔案名稱（可能以 "2-" 或 "1-" 開頭）
    :param file2: 第二個檔案名稱（可能以 "2-" 或 "1-" 開頭）
    :param excel_data: 讀取的 Excel 資料表（DataFrame）
    :return: 如果 LPR 匹配，返回 True；否則返回 False。
    """
    # 在 Excel 中查找 file1 和 file2 對應的 LPR 車牌號碼
    lpr_file1 = excel_data.loc[excel_data['dasequencenum'] == file1, 'plate'].values
    lpr_file2 = excel_data.loc[excel_data['dasequencenum'] == file2, 'plate'].values
    
    # 確認兩者 LPR 是否一致
    if len(lpr_file1) > 0 and len(lpr_file2) > 0:
        return lpr_file1[0] == lpr_file2[0]
    
    return False

# 檢查兩個檔案是否匹配
if check_LPR_match(file1, file2, excel_data):
    print("LPR 匹配成功")
else:
    print("LPR 匹配失敗")