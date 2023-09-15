import re
from common.logger import Log


class IndexSearchParse(object):
    def __init__(self):
        self.logger = Log().get_logger()

    def company_list_search_parse(self, params, response):
        url_list = list()
        html_string = response.text
        url_code_list = re.findall(pattern='https://www.qcc.com/firm/(.*?).html', string=html_string)
        status_content = '公司URL列表搜索解析成功'
        for code in url_code_list:
            url = f"https://www.qcc.com/firm/{code}.html"
            if len(url) != 62 or url in url_list:
                continue
            self.logger.info(f"{params['phone']} {params['company']} {status_content} {url}")
            url_list.append(url)
        url_list_dict = {
            "status": True if len(url_list) > 0 else False, "url_list": url_list, 'status_content': status_content
        }
        return url_list_dict

    def build_company_data(self, company_data):
        company_data['administrative_penalty'] = 'None'
        company_data['environmental_penalty'] = 'None'
        company_data['history_break_faith'] = 'None'
        company_data['history_consumption'] = 'None'
        company_data['history_executor'] = 'None'
        return company_data

    def company_search_parse(self, params, response):
        company_data = {"status": False, 'status_content': '公司不良记录解析失败'}
        html_string = response.text
        if params['company'] not in html_string or params['juridical_person'] not in html_string:
            self.logger.info(f"{params['phone']} {params['company']} 公司不良记录解析失败 公司名称或法人名称不在响应中")
            return self.build_company_data(company_data)
        company_data = {"status": True, 'status_content': '公司不良记录解析成功'}
        re_object = re.search(pattern='"行政处罚".*?"count":(.*?),', string=html_string)
        company_data['administrative_penalty'] = None if re_object is None else re_object.group(1)
        re_object = re.search(pattern='"环保处罚".*?"count":(.*?),', string=html_string)
        company_data['environmental_penalty'] = None if re_object is None else re_object.group(1)
        re_object = re.search(pattern='"历史失信信息".*?"count":(.*?),', string=html_string)
        company_data['history_break_faith'] = None if re_object is None else re_object.group(1)
        re_object = re.search(pattern='"历史限制高消费".*?"count":(.*?),', string=html_string)
        company_data['history_consumption'] = None if re_object is None else re_object.group(1)
        re_object = re.search(pattern='"历史被执行人".*?"count":(.*?),', string=html_string)
        company_data['history_executor'] = None if re_object is None else re_object.group(1)
        self.logger.info(f"{params['phone']} {params['company']} 公司不良记录解析成功 {company_data}")
        return company_data
