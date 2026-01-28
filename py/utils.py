import pandas as pd
import re


# 定義日期轉換函數
def roc_to_datetime(roc_str):
    """將民國年字串 (如 114/12/02 11:39:37) 轉換為 datetime 物件"""
    if pd.isna(roc_str) or not isinstance(roc_str, str):
        return pd.NaT
    try:
        # 移除可能的多餘空白
        roc_str = roc_str.strip()

        # 使用正規表達式提取 年, 月, 日, 時間
        match = re.match(r'(\d+)[/-](\d+)[/-](\d+)\s*(.*)', roc_str)
        if match:
            year, month, day, time_str = match.groups()
            year_ad = int(year) + 1911

            # 組合日期字串
            date_str = f"{year_ad}-{month}-{day}"
            if time_str:
                date_str += f" {time_str}"

            return pd.to_datetime(date_str)
        return pd.NaT
    except:
        return pd.NaT


# 解析工作紀錄簿的時間區間
def parse_work_log_range(range_str):
    """如 114/11/30 22:00 ~ 114/12/01 00:00"""
    try:
        if pd.isna(range_str):
            return pd.NaT, pd.NaT
        parts = range_str.split('~')
        if len(parts) != 2:
            return pd.NaT, pd.NaT
        start = roc_to_datetime(parts[0].strip())
        end = roc_to_datetime(parts[1].strip())
        return start, end
    except:
        return pd.NaT, pd.NaT


# # 提取姓名 (格式通常為 ID-Name，取 - 後面部分)
# def extract_name(s):
#     s = str(s)
#     if '-' in s:
#         return s.split('-')[-1].strip()
#     return s.strip()


# 清理姓名格式
def clean_name(name_str):
    """去除 ID 保留姓名"""
    if pd.isna(name_str): return ""
    name_str = str(name_str).strip()
    if '-' in name_str:
        return name_str.split('-')[-1].strip()
    return name_str
