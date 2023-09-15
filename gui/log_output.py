import time
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTableWidgetItem, QApplication


class LogOutput(object):
    def __init__(self):
        self.index = 0

    def email_log_output(self, table_widget, log_item):
        self.index += 1
        count = 0
        table_widget.insertRow(int(table_widget.rowCount()))
        for keys in log_item:
            value = str(log_item[keys])
            test_object = QTableWidgetItem(value)
            test_object.setTextAlignment(Qt.AlignCenter)
            table_widget.setItem(self.index - 1, count, test_object)
            count += 1
        table_widget.verticalScrollBar().setSliderPosition(self.index)
        QApplication.processEvents()

    def clear_logger(self, table_widget):
        for i in range(self.index):
            table_widget.removeRow(0)  # 删除第i行数据
        # self.ui.tableWidget.clearContents()  # 清除/删除所有内容
        time.sleep(1)
        self.index = 0
