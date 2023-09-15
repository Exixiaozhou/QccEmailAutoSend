import time
import json
import requests
from datetime import datetime
from requests import exceptions as request_exceptions
from common.logger import Log


class TaskRequest(object):
    def __init__(self):
        self.logger = Log().get_logger()

    def request(self, url, method='GET', time_sleep=1.25, max_retry=3, items=None):
        response = {}
        request_result = {'status': False, 'response': response}
        try:
            time.sleep(time_sleep)
            headers = items['headers']
            proxy = items['proxy'] if 'proxy' in items else None
            if method == 'GET' and items['parameter_mode'] is None:
                response = requests.get(url=url, headers=headers, timeout=5)
            elif method == 'GET' and items['parameter_mode'] == 'params' and proxy is None:
                response = requests.get(url=url, headers=headers, params=items['data'], timeout=5)
            elif method == 'GET' and items['parameter_mode'] == 'params' and proxy is not None:
                response = requests.get(url=url, headers=headers, params=items['data'], timeout=5, proxies=proxy)
            elif method == 'POST' and items['parameter_mode'] == 'json' and proxy is None:
                response = requests.post(url=url, headers=headers, json=items['data'], timeout=5)
            elif method == 'POST' and items['parameter_mode'] == 'json' and proxy is not None:
                response = requests.post(url=url, headers=headers, json=items['data'], timeout=5, proxies=proxy)
            elif method == 'POST' and items['parameter_mode'] == 'data' and proxy is None:
                response = requests.post(url=url, headers=headers, data=items['data'], timeout=5)
            elif method == 'POST' and items['parameter_mode'] == 'data' and proxy is not None:
                response = requests.post(url=url, headers=headers, data=items['data'], timeout=5, proxies=proxy)
            elif method == 'PUT' and items['parameter_mode'] == 'data':
                response = requests.put(url=url, headers=headers, data=json.dumps(items['data']))
            # response.raise_for_status()  # 如果响应码不为 200，抛出异常
            request_result['status'] = True
            request_result['response'] = response
            return request_result
        except request_exceptions.ConnectTimeout:
            if type(response) == dict:
                self.logger.info(f'{url}-请求失败 ConnectTimeout 没有响应：{items}!')
            else:
                self.logger.info(f'{url}-请求失败 ConnectTimeout response：{response.text}：{items}!')
        except request_exceptions.RequestException:
            if type(response) == dict:
                self.logger.info(f'{url}-请求失败 RequestException 没有响应：{items}!')
            else:
                if '访问超频' in response.text:
                    status_content = '访问超频,请更新IP代理'
                elif '用户验证' in response.text:
                    status_content = '用户验证,请配置有效的cookie'
                else:
                    status_content = response.text
                self.logger.info(f'{url}-请求失败 RequestException response：{status_content}：{items}!')
        if max_retry > 0:
            return self.request(url=url, method=method, time_sleep=time_sleep, max_retry=max_retry - 1, items=items)
        return request_result

    def get_proxy(self):
        pass
