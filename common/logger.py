import os
import logging
from datetime import datetime
from common.setting import LocalResourcePath


class Log(object):
    logger = logging.getLogger('alter_dicoms_log')  # 创建logging类对象
    logger.setLevel(logging.DEBUG)  # 配置logging对象的默认级别
    """ 创建日志输出格式 可读时间、文件名、打印信息 """
    format_str = '%(asctime)s | %(levelname)s | %(pathname)s | %(funcName)s | 行号：%(lineno)d -> %(message)s'
    formatter = logging.Formatter(format_str)
    log_file_path = os.path.join(LocalResourcePath.LoggerFilePath.value, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    directory_path = os.path.dirname(log_file_path)
    if os.path.exists(directory_path) is False:
        os.makedirs(directory_path)
    file_handler = logging.FileHandler(log_file_path)  # 创建一个写入日志的 dicoms.log 文件
    file_handler.setFormatter(formatter)  # handler对象添加日志输出格式
    file_handler.setLevel(logging.DEBUG)
    terminal_handle = logging.StreamHandler()
    logger.addHandler(file_handler)  # 将logger添加handler对象里面

    def get_logger(self):
        return self.logger  # 将配置好的 logging 对象返回

    def annotation(self):
        """ format 配置：https://www.cnblogs.com/yoyoblogs/p/10948052.html
                %(levelname)s: 打印日志级别名称
                %(pathname)s: 打印当前执行程序的路径
                %(filename)s: 打印当前执行程序名，python如：login.py
                %(funcName)s: 打印日志的当前函数
                %(lineno)d: 打印日志的当前行号,在第几行打印的日志
                %(asctime)s: 打印日志的时间
                %(thread)d: 打印线程ID
                %(threadName)s: 打印线程名称
                %(process)d: 打印进程ID
                %(message)s: 打印日志信息
        """
