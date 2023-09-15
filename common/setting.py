import os
import sys
import random
from enum import Enum
from common.pipeline import DataRead


if getattr(sys, 'frozen', False):
    # 判断当前环境是否为打包环境
    base_path = sys._MEIPASS
else:
    # base_path = os.path.dirname(os.path.abspath("../common"))
    base_path = os.path.abspath(".")


class LocalResourcePath(Enum):
    ResourceDirectory = os.path.join(base_path, 'resource')
    JsEncryptPathW = os.path.join(base_path, os.path.join('resource/js_encrypt', 'encrypt_w.js'))
    JsEncryptPathEpass = os.path.join(base_path, os.path.join('resource/js_encrypt', 'encrypt_epass.js'))
    ExcelDataPath = os.path.join(base_path, os.path.join('resource/data', 'QCC(0714_97834493).xlsx'))
    HtmlTemplateOnePath = os.path.join(base_path, os.path.join('resource/html_template', 'template3.html'))
    WxQrCodeImgPath = os.path.join(base_path, os.path.join('resource/imgs', 'wx_qr_code.jpg'))
    ZsImgPath = os.path.join(base_path, os.path.join('resource/imgs', 'zhengshu.jpg'))
    WxIcoImgPath = os.path.join(base_path, os.path.join('resource/imgs', 'weifeng1.jpg'))
    QccIcoImgPath = os.path.join(base_path, os.path.join('resource/imgs', 'qcc_ico.png'))
    EmailContentIntroducePath = os.path.join(base_path, os.path.join('resource/imgs', 'email_content_introduce.jpg'))

    TestTxtFilePath = os.path.join(base_path, os.path.join('resource/data', 'request_file_upload.txt'))
    GuiFilePath = os.path.join(base_path, os.path.join('resource/gui', 'email_send.ui'))

    # 后续生成的文件
    # FinishCsvFilePath = os.path.join(base_path, os.path.join('resources/data', 'email_finish.csv'))
    # FinishExcelFilePath = os.path.join(base_path, os.path.join('resources/data', 'email_finish.xlsx'))
    # LoggerFilePath = os.path.join(base_path, 'log')
    FinishCsvFilePath = os.path.join('resources/data', 'email_finish.csv')
    FinishExcelFilePath = os.path.join('resources/data', 'email_finish.xlsx')
    LoggerFilePath = 'log'
    ParamSettingPath = os.path.join('resources/data', 'param_setting.json')
    TestHtmlTemplatePath = os.path.join(base_path, os.path.join('resource/html_template', 'test.html'))
    LastlyHtmlTemplatePath = os.path.join(base_path, os.path.join('resource/html_template', 'lastly_template.html'))


class PluginsAccount(Enum):
    dama = {  # 打码平台
        'username': 'xiaozhou', 'password': 'zs1721248377'
    }


class QccCookies(object):
    def __init__(self, cookie_file_path=None):
        """ 企查查 账户cookie配置
            https://www.qcc.com/
            密码：333666feng
        """
        if cookie_file_path is None:
            self.items = None
        else:
            self.pipeline_read = DataRead()
            self.items = self.pipeline_read.cookie_excel_read(cookie_file_path)
            self.phone_list = list(self.items.keys())

    def random_get_cookie(self):
        if self.items is None:
            return {"phone": 'None', "cookie": 'None'}
        else:
            phone = self.phone_list[random.randint(0, len(self.phone_list)-1)]
            return {"phone": phone, "cookie": self.items[phone]}


class EmailAccount(object):
    def __init__(self, email_file_path):
        self.pipeline_read = DataRead()
        self.items = self.pipeline_read.email_excel_read(email_file_path)
        # self.items = {
        #     # '2053216453@qq.com': 'immtadzkvmyhcbjb',
        #     '2393175230@qq.com': 'oinjhgcdsgshdjag',
        #     '3082160195@qq.com': 'vfoqchdtgpncdfca',
        #     '2055427678@qq.com': 'vwldxhlszqrgbidf',
        #     '1725996866@qq.com': 'tiwrfwvgsnyubbag'
        # }
        self.qq_list = list(self.items.keys())

    def random_get_account(self, param, email_send_count_dict):
        number = param['email_account_send_number']
        result = {'status': False, 'status_content': '请添加新的邮箱号和授权码', 'email_address': 'None'}
        for index in range(len(self.qq_list)):
            account = self.qq_list[random.randint(0, len(self.qq_list) - 1)]
            if email_send_count_dict[account] < number:
                result = {"email_address": account, 'status': True, "authorization_code": self.items[account]}
                break
        return result

# print(EmailAccount().random_get_account())
# print(QccCookies().random_get_cookie())
# print(QccCookies().random_get_cookie())
# print(LocalResourcePath.JsEncryptPathW.value)
# print(os.path.exists(LocalResourcePath.JsEncryptPathW.value))
# "企查查-邮件自动发送脚本 作者：小洲 Vx：1721248377"
