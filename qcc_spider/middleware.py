import uuid
import time
import json
import random
import base64
import requests
import datetime


class CommonMiddleware(object):
    def __init__(self):
        pass

    def generate_uuid(self):
        return str(uuid.uuid4())

    def generate_time_stamp(self, number=10):
        if number == 10:
            time_stamp = int(time.time())
        elif number == 13:
            time_stamp = int(time.time() * 1000)
        else:
            time_stamp = int(time.time() * 1000)
        return time_stamp

    def img_verify(self, account, content, typeid):
        print("da")
        content = base64.b64encode(content)
        data = {
            "username": account["username"], "password": account["password"], "typeid": typeid, "image": content,
        }

        response = requests.post("http://api.ttshitu.com/predict", json=data)
        print(response.text)
        # result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)

        # return result


class LoginMiddleware(object):
    def __init__(self):
        pass


class SunProxyMiddleware(object):
    def __init__(self, proxy_url=None, proxy_number=1, seconds=1, tk=None):
        if proxy_url is None:
            self.proxy_url = f'http://http.tiqu.alibabaapi.com/getip?num={proxy_number}&type=2&neek=585986&port=11&lb=1&pb=4&regions='
        else:
            self.proxy_url = proxy_url
        self.tk = tk
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.84 Safari/537.36',
        }
        self.proxy_list = list()
        self.seconds = seconds
        self.total_time = (datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)).strftime('%Y-%m-%d %H:%M:%S')
        self.add_ip_path()
        if proxy_number != 1 and seconds != 1:
            self.parse()

    def parse(self):
        response = requests.get(url=self.proxy_url, headers=self.headers)
        json_data = response.json()['data']
        [self.proxy_list.append({'ip': item['ip'], 'port': item['port']}) for item in json_data]

    def get_proxy(self):
        time.sleep(0.25)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if now_time >= self.total_time:
            self.total_time = (datetime.datetime.now()+datetime.timedelta(seconds=self.seconds)).strftime('%Y-%m-%d %H:%M:%S')
            self.parse()
            self.proxy_list = self.proxy_list[-5:]  # 只保留最新的5个IP代理
            if self.tk is None:
                print("刷新了太阳IP代理：", self.proxy_list)
            else:
                self.tk.common_log_print("刷新了太阳IP代理：", self.proxy_list)
        item = self.proxy_list[random.randint(0, len(self.proxy_list)-1)]
        _proxy = {
            'http': f'http://{item["ip"]}:{item["port"]}',
            'https': f'http://{item["ip"]}:{item["port"]}'
        }
        return _proxy

    def new_get_proxy(self):
        requests_count = 0
        while requests_count < 5:
            response = requests.get(url=self.proxy_url, headers=self.headers)
            # print(response.text)
            json_data = response.json()['data']
            if len(json_data) > 0:
                for item in json_data:
                    ip_port = f"{item['ip']}:{item['port']}"
                    _proxy = {
                        'http': f'http://{ip_port}',
                        'https': f'http://{ip_port}'
                    }
                return _proxy
            time.sleep(2)
            requests_count += 1

    def get_host_ip(self):
        response = requests.get("https://httpbin.org/get")
        host_ip = response.json()['origin']
        return host_ip

    def add_ip_path(self):
        response = requests.get(url=self.proxy_url, headers=self.headers)
        # add_url = 'https://ty-http-d.hamir.net/index/white/add?neek=tyhttp618440&appkey=a053d1d7861979409fccf' \
        #           'df301da7872&white={}'  # 小洲
        add_url = 'https://ty-http-d.hamir.net/index/white/add?neek=tyhttp443999&appkey=8094f086316e2f1d648a1' \
                  'cb0ffb3e173&white={}'  # 熊光
        if '白名单' in response.text:
            print(response.text)
            if "请将" in response.json()['msg'] and '设置' in response.json()['msg']:
                get_host_ip = response.json()['msg'].split('请将')[-1].split('设置')[0]
            else:
                get_host_ip = self.get_host_ip()
            add_response = requests.get(url=add_url.format(get_host_ip), headers=self.headers)
            if self.tk is None:
                print(f"IP白名单添加：{add_response.json()['msg']} - {get_host_ip}")
            else:
                self.tk.common_log_print(f"IP白名单添加：{add_response.json()['msg']} - {get_host_ip}")
        time.sleep(3)


# print(SunProxyMiddleware().new_get_proxy())
