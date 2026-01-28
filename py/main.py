from app_log import log
import os
import sys
import webview
from response import Response
from process import process_audit_files

DEBUG_MODE = False


def get_root_path():
    # 如果是打包後的 exe
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # 如果是開發環境的 .py
    else:
        return os.path.dirname(os.path.abspath(__file__))


# 瀏覽器緩存路徑 (如果你還是想讓 localStorage 生效)
CACHE_DIR = os.path.join(get_root_path(), "web_cache")


class Api:

    def __init__(self):
        self._window = None

    def select_excel(self):
        """
        開啟原生檔案選擇視窗，讓使用者選擇 Excel 檔案。
        回傳選到的檔案路徑。
        """
        # open_file_dialog 回傳的是一個列表 (因為可能多選)，我們只取第一個
        result: list = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=('Excel 文件 (*.xlsx)',)
        )

        if not result:
            error_text = '已取消選擇'
            log().error(error_text)
            raise ValueError(error_text)
        log().info(f'選擇檔案位置：{result[0]}')
        return Response(data={'path': result[0]}).to_dict()  # 回傳絕對路徑字串

    def start(self, data):
        result: list = webview.windows[0].create_file_dialog(
            webview.FileDialog.SAVE,
            save_filename='比對結果.csv',
            file_types=('CSV文件 (*.csv)',)
        )

        if not result:
            error_text = '已取消儲存'
            log().error(error_text)
            raise ValueError(error_text)
        log().info(f'選擇存檔位置：{result[0]}')

        shift_path = data.get('shiftPath')
        log_path = data.get('logPath')
        if not shift_path or not log_path:
            raise ValueError('缺少參數')
        processed_df = process_audit_files(shift_path, log_path)
        processed_df.to_csv(result[0], index=False, encoding='utf-8-sig')
        os.startfile(result[0])


if __name__ == '__main__':
    if DEBUG_MODE:
        log().error('注意！！DEBUG模式已開啟！！')
    log().info('請耐心等待程式開啟......')
    api = Api()
    url = os.path.join(os.getcwd(), './html/index.html') if not DEBUG_MODE else 'http://localhost:5173'
    window = webview.create_window(
        title='日誌稽核小鴿手',
        url=url,
        js_api=api,
        min_size=(800, 500),
        maximized=True,
        confirm_close=True,
    )
    log().debug('程式開啟成功')
    webview.start(
        debug=DEBUG_MODE,
        storage_path=CACHE_DIR,
        private_mode=False,
    )
