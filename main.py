import sys
from PySide2.QtWidgets import QApplication
from gui.email_send_gui import EmailSendGui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    GuiObj = EmailSendGui()
    GuiObj.ui.show()
    sys.exit(app.exec_())

"""
pyinstaller -i qcc.ico -F -w --add-binary common;common --add-binary controller;controller --add-binary email_send;email_send --add-binary gui;gui --add-binary qcc_spider;qcc_spider --add-data resource;resource main.py

https://www.qcc.com/

qcc_email_send_v1.0.exe

脚本需要修改的内容：
一、收件人邮箱，只会发送一次，需要增加判断功能
二、发件人当天的计算次数需要修改, 不应该根据当天的总行数开决定发送次数
三、采集失败的原因
四、gui界面增加采集失败的日志 

"""
