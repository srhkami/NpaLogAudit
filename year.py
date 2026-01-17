import pandas as pd


# 西元轉民國的函式
def ad_to_roc(dt_obj):
    if pd.isnull(dt_obj):  # 預防空值報錯
        return ""

    # 1. 計算民國年 (西元 - 1911)
    roc_year = dt_obj.year - 1911

    # 2. 取得剩下的日期時間字串 (格式：月/日 時:分)
    # %m=兩位數月, %d=兩位數日, %H=24小時制, %M=分
    date_part = dt_obj.strftime("%m/%d %H:%M")

    # 3. 組合在一起 (例如: 114 + / + 12/30 20:00)
    return f"{roc_year}/{date_part}"


# 民國年轉西元年函式
def roc_to_ad(date_str):
    # 假設格式為 "114/12/30 20:00"
    date_part, time_part = date_str.split(' ')
    y, m, d = date_part.split('/')
    ad_year = int(y) + 1911
    return f"{ad_year}-{m}-{d} {time_part}"
