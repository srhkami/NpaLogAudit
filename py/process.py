import pandas as pd
import numpy as np
from utils import roc_to_datetime, clean_name
from shifts import user_shifts


# 主要的處理函數
def process_audit_files(shift_path, log_path):
    with open(log_path, 'rb') as f:
        df = pd.read_excel(f, header=8)

    df['query_name'] = df['使用者'].apply(clean_name)
    df['query_dt'] = df['作業時間'].apply(roc_to_datetime)

    user_intervals = user_shifts(shift_path)

    # 匹配工作紀錄簿 (同時抓取 勤務項目 與 工作記事)
    def get_work_info(row):
        name = row['query_name']
        dt = row['query_dt']

        # 預設回傳兩個空值
        if pd.isna(dt) or name not in user_intervals:
            return pd.Series([None, None])

        intervals, values = user_intervals[name]
        try:
            loc = intervals.get_indexer([dt])[0]
            if loc == -1: return pd.Series([None, None])

            # 找到對應的資料 (duty, note)
            duty, note = values[loc]
            return pd.Series([duty, note])
        except:
            # 處理多重重疊的情況 (較少見，但以防萬一)
            mask = intervals.contains(dt)
            if np.any(mask):
                # 若有多筆，將其串接
                matched_values = values[mask]
                duties = "; ".join([str(v[0]) for v in matched_values if pd.notna(v[0])])
                notes = "; ".join([str(v[1]) for v in matched_values if pd.notna(v[1])])
                return pd.Series([duties, notes])
            return pd.Series([None, None])

    df[['員警工作紀錄簿_勤務項目', '員警工作紀錄簿_工作記事']] = df.apply(get_work_info, axis=1)

    # 移除輔助欄位並存檔
    cols_drop = ['query_name', 'query_dt']
    final_df = df.drop(columns=cols_drop, errors='ignore')

    return final_df
