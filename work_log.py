import pandas as pd


def work_log():
    with open('員警工作紀錄簿.xlsx', 'rb') as f:
        df = pd.read_excel(f, header=2)

    # 3.1 切割時間欄位
    # 使用 '~' 符號將字串切成兩半
    time_split = df['執勤日期時間'].str.split('~', expand=True)

    # 轉換為 datetime 物件
    df['Start_Time'] = time_split[0].str.strip()
    df['End_Time'] = time_split[1].str.strip()

    # 3.2 清理人名 (去除全形空白與前後空白)
    df['記錄人'] = df['記錄人'].astype(str).str.strip()
    df['同班執勤員警'] = df['同班執勤員警'].astype(str).str.strip().replace('nan', '')

    # 3.3 關鍵步驟：變形 (Explode / Unpivot)
    # 我們需要把 "記錄人" 和 "同班執勤員警" 變成同一欄，方便等等去對應 df1 的 "姓名"
    # 我們建立一個暫存表 lookup_table

    # 取出「記錄人」的資料
    part1 = df[['Start_Time', 'End_Time', '記錄人', '工作記事']].rename(columns={'記錄人': '姓名_key'})

    # 取出「同班執勤員警」的資料 (並過濾掉沒有同班員警的空資料)
    part2 = df[['Start_Time', 'End_Time', '同班執勤員警', '工作記事']].rename(columns={'同班執勤員警': '姓名_key'})
    part2 = part2[part2['姓名_key'] != '']  # 去除空值

    # 合併兩者，建立完整的對照表
    lookup_df = pd.concat([part1, part2], ignore_index=True)

    return lookup_df
