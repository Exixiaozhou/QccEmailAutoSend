import os
from datetime import datetime
from common.pipeline import DataRead, DataSave
from common.setting import LocalResourcePath, EmailAccount
from qcc_spider.controller import IndexSearchController
from email_send.controller import QqEmailSendController
from common.logger import Log


class Runs(object):
    def __init__(self, params_items):
        self.email_finish_file = LocalResourcePath.FinishCsvFilePath.value
        self.pipeline_read = DataRead()
        self.pipeline_save = DataSave()
        self.init_csv_file()
        self.qcc_spider = IndexSearchController(params_items['cookie'])
        self.qq_email_send = QqEmailSendController()
        self.email_account = EmailAccount(params_items['email'])
        self.email_send_count_dict = self.init_send_count()
        self.logger = Log().get_logger()

    def init_send_count(self):
        file_path = LocalResourcePath.FinishExcelFilePath.value
        send_count = {}
        if os.path.exists(file_path) is True:
            send_count = self.pipeline_read.send_finish_excel_read(file_path)
        for keys in self.email_account.qq_list:
            if keys not in send_count:
                send_count[keys] = 0
        return send_count

    def data_verify(self, task_result):
        data = task_result['company_data']
        status = False
        if data['status'] is True:
            del data['status']  # 把status字段删除
            for keys in data:
                value = data[keys]
                if value is None or int(value) < 1:
                    continue
                status = True
            task_result['company_data']['status_content'] = '公司黑料数据全部为0'
        if status is False:  # 如果请求失败或数据为None、全为0则失败
            self.data_save([task_result])
        return status

    def get_logger_items(self, data):
        params = data['params']
        company_data = data['company_data']
        qq_account = data['qq_account']
        logger_items = {
            'one': params['phone'], 'two':  params['company'], 'three': params['juridical_person'],
            'four': ','.join(params['email_address_list']).replace(',', ';'),
            'five': company_data['administrative_penalty'], 'six': company_data['environmental_penalty'],
            'seven': company_data['history_break_faith'], 'eight': company_data['history_consumption'],
            'nine': company_data['history_executor'], 'ten': qq_account['email_address'],
            'eleven': str(self.email_send_count_dict[qq_account['email_address']])
        }
        return logger_items

    def controller(self, data):
        gui = data['gui']
        task_result = self.qcc_spider.runs(params=data, flag=True)  # 调用企查查数据采集操作
        task_result['qq_account'] = self.email_account.random_get_account(data, self.email_send_count_dict)
        if task_result['qq_account']['status'] is False:
            task_result['status_content'] = task_result['qq_account']['status_content']
            task_result['logger_items']['twelve'] = task_result['qq_account']['status_content']
            gui.gui_log_object.email_log_output(gui.ui.emailSendTableWidget, task_result['logger_items'])
            self.data_save(company_data_list=[task_result], label='qcc_spider')
            return False
        else:
            self.data_save(company_data_list=[task_result], label='qcc_spider')
        if task_result['company_data']['status'] is False:  # 数据采集失败，或者不需要发送邮箱
            return False
        self.email_send_count_dict[task_result['qq_account']['email_address']] += 1
        send_result = self.qq_email_send.runs(task_result, self.email_send_count_dict)  # 调用发送邮箱操作
        task_result['status_content'] = "发送成功" if send_result is True else "发送异常"
        self.data_save([task_result])
        return True

    def init_csv_file(self):
        directory_path = os.path.dirname(self.email_finish_file)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)
        if os.path.exists(self.email_finish_file) is True:
            return True
        title_content = '企业名称,法定代表人,邮箱,行政处罚,环保处罚,历史失信信息,历史限制高消费,历史被执行人,发送人邮箱,当天总发送次数,状态,日期\n'
        self.pipeline_save.create_file(self.email_finish_file, title_content)

    def data_save(self, company_data_list, label='email_send'):
        current_datetime = datetime.now().strftime('%Y-%m-%d')
        for item in company_data_list:
            params = item['params']
            company_data = item['company_data']
            qq_account = item['qq_account']
            email_content = ','.join(params['email_address_list']).replace(',', ';')
            content = f"{params['company']},{params['juridical_person']},{email_content},"
            content += f"{company_data['administrative_penalty']},{company_data['environmental_penalty']},"
            content += f"{company_data['history_break_faith']},{company_data['history_consumption']},"
            content += f"{company_data['history_executor']},{qq_account['email_address']},"
            number = self.email_send_count_dict[qq_account['email_address']] if label == 'email_send' else 'None'
            content += f"{number},{item['status_content']},{current_datetime}\n"
            self.pipeline_save.csv_save(self.email_finish_file, content)
            self.logger.info(f"写入成功：{content}")
        self.pipeline_save.csv_save_as_xlsx(self.email_finish_file)
        return True

    def runs(self, params):
        self.controller(params)


# if __name__ == '__main__':
#     Runs().runs()

