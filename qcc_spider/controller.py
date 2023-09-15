
from common.setting import QccCookies
from qcc_spider.parse import IndexSearchParse
from qcc_spider.request import IndexSearchRequest


class IndexSearchController(object):
    def __init__(self, cookie_file_path=None):
        self.qcc_cookies = QccCookies(cookie_file_path)
        self.index_search_parse = IndexSearchParse()
        self.index_search_request = IndexSearchRequest()
        self.keyword_list = [
            'administrative_penalty', 'environmental_penalty', 'history_break_faith', 'history_consumption',
            'history_executor'
        ]

    def company_list_search_controller(self, params):
        """ 公司列表搜索 return 公司url的list """
        request_result = self.index_search_request.company_list_search_request(params)
        if request_result['status'] is False:
            request_result['url_list'] = []
            return request_result
        url_list_dict = self.index_search_parse.company_list_search_parse(params, request_result["response"])
        return url_list_dict

    def company_search_controller(self, params, company_data, url_list, index=0):
        company_data["status"], company_data["status_content"] = False, "公司url搜索请求完毕"
        if index + 1 > len(url_list):  # 如果url数量小于1
            return company_data
        params['url'] = url_list[index]  # 从0开始取出url
        request_result = self.index_search_request.company_search_request(params)
        if request_result['status'] is False:
            company_data['status_content'] = request_result['status_content']
            return company_data
        parse_result = self.index_search_parse.company_search_parse(params, request_result["response"])
        if parse_result['status'] is False:
            self.company_search_controller(params, company_data, url_list, index+1)  # 递归调用
        return parse_result

    def data_verify(self, data):
        """ 判断解析成功的数据是否需要发送邮箱，并返回是否需要发送的状态 """
        if data['status'] is True:
            data['status'] = False  # 如果请求失败或数据为None、全为0则失败, 不需要发送邮箱
            for keys in data:
                if keys not in self.keyword_list:
                    continue
                value = data[keys]
                if value is None or value == 'None' or int(value) < 1:
                    continue
                data['status'] = True
                break
            else:
                data['status_content'] = '公司不良记录数据全部为0' if data['status'] is False else data['status_content']
        return data

    def get_logger_items(self, params, company_data):
        logger_items = {
            'one': params['phone'], 'two':  params['company'], 'three': params['juridical_person'],
            'four': ','.join(params['email_address_list']).replace(',', ';'),
            'five': company_data['administrative_penalty'], 'six': company_data['environmental_penalty'],
            'seven': company_data['history_break_faith'], 'eight': company_data['history_consumption'],
            'nine': company_data['history_executor'], 'ten': 'None', 'eleven': 'None',
            'twelve': company_data['status_content']
        }
        return logger_items

    def build_company_data(self):
        company_data = {"status": True, 'status_content': '取消企查查数据采集步骤'}
        company_data['administrative_penalty'] = 'None'
        company_data['environmental_penalty'] = 'None'
        company_data['history_break_faith'] = 'None'
        company_data['history_consumption'] = 'None'
        company_data['history_executor'] = 'None'
        return company_data

    def runs(self, params, flag=False):
        gui = params['gui']
        cookie_result = self.qcc_cookies.random_get_cookie()
        params['phone'] = cookie_result['phone']
        params['cookie'] = cookie_result['cookie']
        if flag is True:
            company_data_dict = self.build_company_data()
            logger_items = self.get_logger_items(params, company_data_dict)
            return {
                "params": params, 'company_data': company_data_dict, 'logger_items': logger_items,
                'status_content': company_data_dict['status_content']
            }
        url_list_dict = self.company_list_search_controller(params=params)
        company_data_dict = self.index_search_parse.build_company_data(url_list_dict)
        logger_items = self.get_logger_items(params, company_data_dict)
        gui.gui_log_object.email_log_output(gui.ui.emailSendTableWidget, logger_items)
        if url_list_dict['status'] is False:
            return {
                "params": params, 'company_data': company_data_dict, 'logger_items': logger_items,
                'status_content': company_data_dict['status_content']
            }
        company_data = self.company_search_controller(params, company_data_dict, company_data_dict['url_list'])
        logger_items = self.get_logger_items(params, company_data)
        gui.gui_log_object.email_log_output(gui.ui.emailSendTableWidget, logger_items)
        company_data = self.data_verify(company_data)
        return {
            "params": params, 'company_data': company_data, 'logger_items': logger_items,
            'status_content': company_data['status_content']
        }


# IndexSearchController().runs()
