import json
import random
import requests
from common.setting import PluginsAccount
from qcc_spider.constants import WebHeaders, LoginUrl
from qcc_spider.middleware import LoginMiddleware, CommonMiddleware

# with open(file='encrypt.js', mode='r', encoding='utf-8') as fis:
#     js_code = fis.read()
# js_obj = execjs.compile(js_code)  # 激将JS代码传入
# result = js_obj.call('get_epass', '1224142124')  # 调用JS的函数, 参数1：函数名、参数2：该函数所需要的参数
# print(result)


class Login(object):
    def __init__(self):
        self.login_middleware = LoginMiddleware()
        self.common_middleware = CommonMiddleware()
        self.dama_account = PluginsAccount.dama.value

    def gcaptcha4_load(self):
        url = LoginUrl.get.value['gcaptcha4_load']
        headers = WebHeaders.get.value
        form_data = {
            'captcha_id': '8daf8b2d78f74aea6a77c0d10da77d41',
            'challenge': self.common_middleware.generate_uuid(),
            'client_type': 'web', 'lang': 'zh-cn',
            'callback': f"geetest_{self.common_middleware.generate_time_stamp(13)}"
        }
        response = requests.get(url=url, headers=headers, params=form_data)
        json_content = response.text.split(f"{form_data['callback']}(")[-1][:-1]
        json_data = json.loads(json_content)['data']
        img_url = json_data['bg'] if json_data['captcha_type'] == 'slide' else json_data['imgs']
        param_items = {
            "lot_number": json_data['lot_number'], 'payload': json_data['payload'],
            'process_token': json_data['process_token'], 'datetime': json_data['pow_detail']['datetime'],
            "captcha_type": json_data['captcha_type'], 'img_url': f'https://static.geetest.com/{img_url}',
        }
        return param_items

    def build_param_w(self, param):
        url = param['img_url']
        headers = WebHeaders.get.value
        response = requests.get(url=url, headers=headers)
        img_content = response.content
        dama_type_id = 53 if param['captcha_type'] == 'slide' else 20
        self.common_middleware.img_verify(self.dama_account, img_content, dama_type_id)
        e = {
            "pass_time": random.randint(5000, 10000), "userresponse": [[6770, 4002], [735, 5269], [8701, 1830]],
            "device_id": "05c041505610c5f2ed1270b81ef83af6", "lot_number": param["lot_number"],
            "pow_msg": f"1|0|md5|{param['datetime']}|8daf8b2d78f74aea6a77c0d10da77d41|{param['lot_number']}||e032eed881ea7355",
            "powSign": "db73bc611a7f3069a53f80207c4760c3"
        }

    def gcaptcha4_verify(self, param):
        url = LoginUrl.get.value['gcaptcha4_verify']
        headers = WebHeaders.get.value
        w = self.build_param_w(param)
        form_data = {
            'callback': f"geetest_{self.common_middleware.generate_time_stamp(13)}",
            'captcha_id': '8daf8b2d78f74aea6a77c0d10da77d41', 'client_type': 'web',
            'lot_number': param['lot_number'], 'payload': param['payload'],
            'process_token': param['process_token'], 'payload_protocol': 1,
            'pt': 1, 'w': ''
        }

    def runs(self):
        param_items = self.gcaptcha4_load()
        self.gcaptcha4_verify(param_items)


if __name__ == "__main__":
    Login().runs()

