import os
import random
import time
import threading
import subprocess
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QFileDialog, QMessageBox
from controller.running_thread import EmailSendThread
from common.setting import LocalResourcePath
from common.pipeline import DataRead, DataSave


class WidgetInit(object):
    def __init__(self, gui):
        self.gui = gui

        self.pipeline_read = DataRead()
        self.pipeline_save = DataSave()

        # 变量定义
        self.file_import_object = {
            self.gui.excel_label: {  # excel表格文件路径路径
                'path': None, 'input_text': None, 'line_edit': self.gui.ui.qccExcelFileInput
            },
            self.gui.cookie_label: {  # 企查查cookie文件路径
                'path': None, 'input_text': None, 'line_edit': self.gui.ui.qccCookieFileInput
            },
            self.gui.email_label: {  # 邮箱文件路径
                'path': None, 'input_text': None, 'line_edit': self.gui.ui.qqEmailFileInput
            },
            self.gui.accessory_label: {  # 附件目录
                'file_path': None, 'input_text': None, 'line_edit': self.gui.ui.accessoryDirectoryInput
            }
        }
        self.email_account_send_number = random.randint(40, 50)
        self.param_setting_object = {
            self.gui.email_send_all_number_label: {
                'value': 300,  'input_text': None, 'line_edit': self.gui.ui.emailSendAllNumberInput
            },
            self.gui.email_account_send_number_label: {
                'value': self.email_account_send_number, 'input_text': None,
                'line_edit': self.gui.ui.emailAccountSendNumberInput
            }
        }
        self.param_setting_path = LocalResourcePath.ParamSettingPath.value

    def widget_setting(self):
        # 设置ico、另外定义外观
        icon = QIcon(self.gui.qcc_ico_dir)
        self.gui.ui.setWindowIcon(icon)  # 设置ico
        # 设置行号可见, 显示tableWidget标题
        self.gui.ui.emailSendTableWidget.horizontalHeader().setVisible(True)
        self.gui.ui.emailSendTableWidget.verticalHeader().setVisible(True)
        email_content_img = LocalResourcePath.EmailContentIntroducePath.value
        pixmap = QPixmap(email_content_img)  # 添加微信图片
        self.gui.ui.email_content_label.setPixmap(pixmap)

    def button_connect_init(self):
        # 企查查数据采集、邮箱自动发送操作按钮绑定
        self.gui.ui.emailSendStartButton.clicked.connect(
            self.gui.button_function.email_send_running
        )
        self.gui.ui.emailSendStopButton.clicked.connect(
            lambda: self.thread_it(self.gui.button_function.email_stop_running)
        )
        self.gui.ui.emailSendClearLoggerButton.clicked.connect(
            lambda: self.thread_it(self.gui.button_function.clear_logger)
        )
        self.gui.ui.emailSendExitButton.clicked.connect(
            lambda: self.thread_it(self.gui.button_function.exit_program)
        )
        # 文件导入按钮绑定
        self.gui.ui.qccExcelFileInputButton.clicked.connect(lambda: self.file_import(self.gui.excel_label))
        self.gui.ui.qccCookieFileInputButton.clicked.connect(lambda: self.file_import(self.gui.cookie_label))
        self.gui.ui.qqEmailFileInputButton.clicked.connect(lambda: self.file_import(self.gui.email_label))
        self.gui.ui.accessoryDirectoryInputButton.clicked.connect(lambda: self.directory_import(self.gui.accessory_label))

    def thread_it(self, func, *args):
        '''
            将函数打包进线程
        '''
        self.myThread = threading.Thread(target=func, args=args)
        self.myThread.setDaemon(True)
        self.myThread.start()

    def file_import(self, label_name):
        # 打开文件对话框, 选择文件
        self.file_import_object[label_name]['path'], _ = QFileDialog.getOpenFileName(
            self.gui.ui, "选择文件", "", "All Files (*);;Text Files (*.txt)"
        )
        # 输出选择的文件路径和目录路径
        self.file_import_object[label_name]['line_edit'].setText(self.file_import_object[label_name]['path'])

    def directory_import(self, label_name):
        self.file_import_object[label_name]['path'] = QFileDialog.getExistingDirectory(self.gui.ui, "选择目录", "")
        self.file_import_object[label_name]['line_edit'].setText(self.file_import_object[label_name]['path'])

    def init_param_setting(self):
        json_data = self.pipeline_read.json_read(self.param_setting_path)
        for label_name in self.file_import_object:
            if label_name not in json_data:
                continue
            value = json_data[label_name]
            self.file_import_object[label_name]['path'] = value
            self.file_import_object[label_name]['line_edit'].setText(value)
        for label_name in self.param_setting_object:
            if label_name not in json_data:
                continue
            value = json_data[label_name]
            self.param_setting_object[label_name]['value'] = value
            self.param_setting_object[label_name]['line_edit'].setText(str(value))

    def running_init(self):
        if os.path.exists(self.param_setting_path) is True:
            self.init_param_setting()
        self.widget_setting()
        self.button_connect_init()


class EmailSendButtonController(object):
    def __init__(self, gui):
        self.gui = gui
        self.email_thread = None
        self.logger_item = {
            'one': '-' * 20, 'two': '-' * 20, 'three': '-' * 20, 'four': '-' * 20, 'five': '-' * 20,
            'six': '-' * 20, 'seven': '-' * 20, 'eight': '-' * 20, 'nine': '-' * 20, 'ten': '-' * 20, 'eleven': '-' * 20
        }
        self.param_check_object = {
            self.gui.excel_label: '企查查公司邮箱表格没有导入,请点击浏览按钮进行导入！',
            # self.gui.cookie_label: '企查查cookie表格没有导入,请点击浏览按钮进行导入！',
            self.gui.email_label: '发送人邮箱授权码表格没有导入,请点击浏览按钮进行导入！',
        }
        self.param_check = ParamsCheck(self.gui)

    def email_send_running(self):
        check_result = self.param_check.runs(self.param_check_object)
        if check_result['status'] is False:
            return False
        self.logger_item['twelve'] = '程序已经开始运行，请勿多次点击开始运行按钮'
        self.gui.gui_log_object.email_log_output(self.gui.ui.emailSendTableWidget, self.logger_item)
        self.email_thread = EmailSendThread(self.gui, check_result)
        self.email_thread.start()

    def email_stop_running(self):
        self.email_thread.stop()
        self.logger_item['twelve'] = '程序已设置停止线程，请等待最后一个账号运行完再进行下一步操作'
        self.gui.gui_log_object.email_log_output(self.gui.ui.emailSendTableWidget, self.logger_item)

    def clear_logger(self):
        self.gui.gui_log_object.clear_logger(self.gui.ui.emailSendTableWidget)

    def exit_program(self):
        tmp = os.popen("tasklist").readlines()
        for tm in tmp:
            if 'python' not in tm and 'demo_gui' not in tm and 'qcc_email_send' not in tm and 'main' not in tm:
                continue
            self.logger_item['twelve'] = f'进程杀死成功：{tm}'
            self.gui.gui_log_object.email_log_output(self.gui.ui.emailSendTableWidget, self.logger_item)
            time.sleep(0.5)
            pid = tm.strip().replace(' ', '').split('.exe')[-1].split('Console')[0]
            subprocess.Popen("taskkill /F /T /PID " + str(pid), shell=True)
        return True


class ParamsCheck(object):
    def __init__(self, gui):
        self.gui = gui
        self.pipeline_save = DataSave()
        self.param_setting_path = LocalResourcePath.ParamSettingPath.value

    def show_message_box(self, tip_content):
        QMessageBox.warning(self.gui.ui, "警告", tip_content, QMessageBox.Ok)
        # message_box = QMessageBox()
        # message_box.setText(tip_content)
        # message_box.setWindowTitle("小洲友情提示")
        # # message_box.setIcon(QMessageBox.Warning)  # 设置图标为警告图标
        # message_box.setWindowFlags(message_box.windowFlags() | 0x00000008)
        # # message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # message_box.exec_()

    def file_check(self, label, tip_content):
        path_items = self.gui.widget_init.file_import_object[label]
        result = {'status': False}
        if path_items['path'] is None or len(path_items['path'].strip()) < 2:
            QMessageBox.warning(self.gui.ui, "警告", tip_content, QMessageBox.Ok)  # 提示框的地方不能有线程
        else:
            result = {'status': True, 'path': path_items['path']}
        return result

    def setting_check(self, label):
        param_items = self.gui.widget_init.param_setting_object[label]
        value = param_items['line_edit'].text().strip()
        value = int(value) if len(value) > 0 else param_items['value']
        self.gui.widget_init.param_setting_object[label]['value'] = value
        return value

    def email_file_check(self):
        pass

    def qcc_file_check(self):
        pass

    def controller(self, file_check_object):
        setting_items = {'status': False}
        for keys in file_check_object:
            tip_content = file_check_object[keys]
            task_result = self.file_check(keys, tip_content)
            if task_result['status'] is False:
                return setting_items
            setting_items[keys] = task_result['path']
        for key in self.gui.widget_init.param_setting_object:
            setting_items[key] = self.setting_check(key)
        del setting_items['status']
        self.pipeline_save.json_save(self.param_setting_path, setting_items)
        setting_items['status'] = True
        return setting_items

    def runs(self, file_check_object):
        setting_items = self.controller(file_check_object)
        setting_items['cookie'] = None
        return setting_items

    def thread_it(self, func, *args):
        '''
            将函数打包进线程
        '''
        self.myThread = threading.Thread(target=func, args=args)
        self.myThread.setDaemon(True)
        self.myThread.start()
