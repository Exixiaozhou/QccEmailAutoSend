# 打包命令
pyinstaller -i qcc.ico -F -w --add-binary common;common --add-binary controller;controller --add-binary email_send;email_send --add-binary gui;gui --add-binary qcc_spider;qcc_spider --add-data resource;resource main.py

作者的CSDN主页：https://blog.csdn.net/EXIxiaozhou；
