import pandas as pd
from year import ad_to_roc, roc_to_ad


def check_book():
    with open('出入登記簿.xlsx', 'rb') as f:
        df = pd.read_excel(f, header=2)

    # 應用轉換並變為 datetime 物件
    df['日期時間'] = (df['日期時間']).apply(roc_to_ad)
    df['日期時間'] = pd.to_datetime(df['日期時間'])

    # --- 核心配對邏輯 ---

    pair_results = []

    # 依照 [姓名, 勤務內容] 分組，這能確保我們只在同一個人的同一個任務中找配對
    # 並且依照 [時間] 排序，確保先發生的是出勤
    grouped = df.sort_values('日期時間').groupby(['姓名', '勤務項目'])

    for (name, task), group in grouped:
        start_time = None

        for _, row in group.iterrows():
            status = row['類型']
            current_time = row['日期時間']

            if status == '出勤':
                # 記錄開始時間，等待下一次退勤
                start_time = current_time

            elif status == '退勤':
                # 只有當我們手上有一個 "待配對" 的出勤時間，才進行配對
                if start_time is not None:
                    # 找到一組完整資料，存入結果
                    pair_results.append({
                        '姓名': name,
                        '勤務項目': task,
                        '出勤時間': start_time,
                        '退勤時間': current_time,
                        # 計算工時 (小時)
                        '時數': (current_time - start_time).total_seconds() / 3600
                    })
                    # 配對完成後，將 start_time 重置，準備抓下一組
                    start_time = None
                else:
                    # 這是「有退勤但沒出勤」的異常狀況，通常忽略
                    pass

        # 迴圈結束後，如果 start_time 仍然不是 None，代表這筆出勤沒有退勤資料
        # 因為我們沒有 append 到 results，所以它自動被排除了 (達成需求3)

    # --- 輸出結果 ---
    result_df = pd.DataFrame(pair_results)

    # 格式化時間顯示 (可選)
    result_df['出勤時間'] = result_df['出勤時間'].apply(ad_to_roc)
    result_df['退勤時間'] = result_df['退勤時間'].apply(ad_to_roc)

    return result_df
