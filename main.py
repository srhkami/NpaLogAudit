import pandas as pd
from check_book import check_book
from work_log import work_log

if __name__ == "__main__":
    check_book_df = check_book()
    work_log_df = work_log()

    # ---------------------------------------------------------
    # 4. 進行核對 (Merge)
    # ---------------------------------------------------------

    # 將 df1 與 lookup_df 進行合併
    # 左邊(df1)用: ['出勤時間', '退勤時間', '姓名']
    # 右邊(lookup)用: ['Start_Time', 'End_Time', '姓名_key']

    merged_df = pd.merge(
        check_book_df,
        work_log_df,
        left_on=['出勤時間', '退勤時間', '姓名'],
        right_on=['Start_Time', 'End_Time', '姓名_key'],
        how='left'  # left join: 保留 df1 原本所有資料，沒對應到的記事補空值
    )

    # ---------------------------------------------------------
    # 5. 整理最終欄位
    # ---------------------------------------------------------

    # 刪除多餘的輔助欄位 (Start_Time, End_Time, 姓名_key)
    final_result = merged_df.drop(columns=['Start_Time', 'End_Time', '姓名_key'])

    print("--- 核對完成後的表格 ---")
    print(final_result[['姓名', '勤務項目', '出勤時間', '退勤時間', '工作記事']])

    final_result.to_excel("勤務比對完成表.xlsx", index=False, sheet_name="sheet")
