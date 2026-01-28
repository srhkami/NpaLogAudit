import pandas as pd
import re
import numpy as np
from utils import parse_work_log_range, clean_name


# 讀取員警工作紀錄簿預先處理
def user_shifts(shift_path):
    user_intervals = {}  # 存放每個人的工作時段 (包含主記錄人與同班員警)
    with open(shift_path, 'rb') as f:
        work_df = pd.read_excel(f, header=2)

    if work_df is None:
        raise ValueError('沒有選擇工作記錄簿！')

    # 去除欄位名稱的空白
    work_df.columns = [c.strip() for c in work_df.columns]

    # 確保所需欄位存在 (包含勤務項目)
    target_cols = ['執勤日期時間', '記錄人', '同班執勤員警', '勤務項目', '工作記事']
    for c in target_cols:
        if c not in work_df.columns:
            work_df[c] = None

    # 解析時間
    ranges = work_df['執勤日期時間'].apply(lambda x: pd.Series(parse_work_log_range(x)))
    work_df['start_dt'] = ranges[0]
    work_df['end_dt'] = ranges[1]
    work_df = work_df.dropna(subset=['start_dt', 'end_dt'])

    # --- 展開記錄人與同班員警 ---
    expanded_work_list = []

    for _, row in work_df.iterrows():
        start = row['start_dt']
        end = row['end_dt']
        duty = row['勤務項目']  # 抓取勤務項目
        note = row['工作記事']

        # 1. 處理記錄人
        recorder = clean_name(row['記錄人'])
        if recorder:
            expanded_work_list.append({
                'name': recorder,
                'start': start,
                'end': end,
                'duty': duty,
                'note': note
            })

        # 2. 處理同班執勤員警
        co_officers = str(row['同班執勤員警'])
        if co_officers and co_officers.lower() != 'nan':
            names = re.split(r'[ ,、;]+', co_officers)
            for name in names:
                clean_n = clean_name(name)
                if clean_n:
                    expanded_work_list.append({
                        'name': clean_n,
                        'start': start,
                        'end': end,
                        'duty': duty,
                        'note': note
                    })

    # 建立索引 (儲存 duty 和 note)
    expanded_df = pd.DataFrame(expanded_work_list)
    if not expanded_df.empty:
        for user, group in expanded_df.groupby('name'):
            try:
                intervals = pd.IntervalIndex.from_arrays(group['start'], group['end'], closed='both')
                # 存入 tuple (勤務項目, 工作記事)
                values = list(zip(group['duty'], group['note']))
                user_intervals[user] = (intervals, np.array(values, dtype=object))
            except Exception as e:
                pass

    return user_intervals
