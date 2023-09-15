from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QMessageBox
from common.setting import LocalResourcePath
from gui.widget_init import WidgetInit, EmailSendButtonController
from gui.log_output import LogOutput


class EmailSendGui(QWidget):
    def __init__(self):
        super().__init__()
        self.ui_file_path = LocalResourcePath.GuiFilePath.value
        self.qcc_ico_dir = LocalResourcePath.QccIcoImgPath.value

        qt_file_object = QFile(self.ui_file_path)
        qt_file_object.open(QFile.ReadOnly)
        qt_file_object.close()
        self.ui = QUiLoader().load(qt_file_object)

        # 文件，目录导入的标签
        self.excel_label = 'excel'
        self.cookie_label = 'cookie'
        self.email_label = 'email'
        self.accessory_label = 'accessory'

        # 邮箱运行数量, 参数配置
        self.email_send_all_number_label = 'email_send_all_number'
        self.email_account_send_number_label = 'email_account_send_number'

        # 创建组件初始化类、按钮绑定类型、并调用方法
        self.button_function = EmailSendButtonController(self)
        self.widget_init = WidgetInit(self)
        self.widget_init.running_init()
        self.gui_log_object = LogOutput()


