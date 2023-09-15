import time
import threading
from common.setting import LocalResourcePath
from common.pipeline import DataRead
from controller.runs import Runs
from common.logger import Log
from qcc_spider.middleware import SunProxyMiddleware


class EmailSendThread(threading.Thread):
    def __init__(self, gui, check_result):
        super().__init__()
        self.gui = gui
        self.params_items = check_result
        self._stop_event = threading.Event()
        self.pipeline_read = DataRead()
        self.logger = Log().get_logger()
        self.run_object = Runs(self.params_items)
        # self.proxy_middleware = SunProxyMiddleware()

    def stop(self):
        self._stop_event.set()

    def run(self):
        finish_file_path = LocalResourcePath.FinishExcelFilePath.value
        file_path = self.params_items['excel']
        excel_data = self.pipeline_read.qcc_excel_read(file_path, finish_file_path)
        # proxy = self.proxy_middleware.new_get_proxy()
        for params in excel_data[:self.params_items['email_send_all_number']]:
            if self._stop_event.is_set() is True:  # 当停止按钮被点击后则会进入这个跳出循环条件
                break
            params['gui'] = self.gui
            params['email_account_send_number'] = self.params_items['email_account_send_number']
            # params['proxy'] = proxy
            self.run_object.runs(params)
            self.logger.info(f"任务添加成功: {params}")
            time.sleep(2)
        logger_item = {
            'one': '-' * 20, 'two': '-' * 20, 'three': '-' * 20, 'four': '-' * 20, 'five': '-' * 20,
            'six': '-' * 20, 'seven': '-' * 20, 'eight': '-' * 20, 'nine': '-' * 20, 'ten': '-' * 20,
            'eleven': '-' * 20, "twelve":  '程序已经停止运行,请进行下一步操作'
        }
        self.gui.gui_log_object.email_log_output(self.gui.ui.emailSendTableWidget, logger_item)
