import time
import json
import random
import requests
from requests import exceptions as request_exceptions
from qcc_spider.constants import IndexSearchUrl, WebHeaders
from common.utils import TaskRequest
from common.logger import Log


class IndexSearchRequest(object):
    def __init__(self):
        self.request_service = TaskRequest()
        self.logger = Log().get_logger()

    def company_list_search_request(self, items):
        url = IndexSearchUrl.get.value['index_url']
        headers = WebHeaders.get.value
        headers['cookie'] = items['cookie']
        form_data = {"key": items['company']}
        params = {'data': form_data, 'parameter_mode': 'params', 'headers': headers}
        time_sleep = random.randint(6, 10)
        request_result = self.request_service.request(url=url, method='GET', time_sleep=time_sleep, items=params)
        result = {"status": False, 'response': request_result['response']}
        log_content = f"{items['phone']} {items['company']} 公司URL列表搜索 "
        if request_result['status'] is True:
            response = request_result['response']
            if '用户验证' in response.text:
                log_content += f"-请求失败 用户验证 请配置有效的cookie"
                result['status_content'] = "公司URL列表搜索 用户验证 请配置有效的cookie"
            elif '访问超频' in response.text:
                log_content += f"-请求失败 访问超频 请更新IP代理"
                result['status_content'] = "公司URL列表搜索 访问超频 请更新IP代理"
            else:
                result['status'] = True
                result['status_content'] = "公司URL列表搜索 请求成功"
                log_content += f"-请求成功"
        else:
            log_content += f"-请求失败 连续请求不成功"
            result['status_content'] = "公司URL列表搜索 连续请求不成功"
        self.logger.info(log_content)
        return result

    def company_search_request(self, items):
        url = items['url']
        headers = WebHeaders.get.value
        headers['cookie'] = items['cookie']
        params = {'data': None, 'parameter_mode': None, 'headers': headers}
        time_sleep = random.randint(6, 10)
        request_result = self.request_service.request(url=url, method='GET', time_sleep=time_sleep, items=params)
        result = {"status": False, 'response': request_result['response']}
        log_content = f"{items['phone']} {items['company']} 公司数据搜索搜索 "
        if request_result['status'] is True:
            response = request_result['response']
            if '用户验证' in response.text:
                log_content += f"-请求失败 用户验证 请配置有效的cookie"
                result['status_content'] = "公司URL列表搜索 用户验证、请配置有效的cookie"
            elif '访问超频' in response.text:
                log_content += f"-请求失败 访问超频 请更新IP代理"
                result['status_content'] = "公司URL列表搜索 访问超频、请更新IP代理"
            else:
                result['status'] = True
                result['status_content'] = "公司数据搜索搜索 请求成功"
                log_content += f"-请求成功"
        else:
            log_content += f"-请求失败 连续请求不成功"
            result['status_content'] = "公司数据搜索搜索 连续请求不成功"
        self.logger.info(log_content)
        return result
