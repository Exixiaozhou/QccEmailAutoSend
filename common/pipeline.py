import os
import time
import json
import pandas as pd
from datetime import datetime


class DataRead(object):
    def __init__(self):
        pass

    def get_finish_company_list(self, file_path):
        finish_company_list = list()
        if os.path.exists(file_path) is False:
            return finish_company_list
        df = pd.read_excel(io=file_path, skiprows=0, usecols=None)
        for index, row in df.iterrows():
            if row['状态'] == '发送成功':
                finish_company_list.append(row["企业名称"])
        return finish_company_list

    def qcc_excel_read(self, file_path, finish_file_path):
        df = pd.read_excel(io=file_path, skiprows=0, usecols=None)
        finish_company_list = self.get_finish_company_list(finish_file_path)
        excel_data = list()
        for index, row in df.iterrows():
            company = row["企业名称"]
            if company in finish_company_list:  # 如果该公司已经被发送过一次，则不做存储
                continue
            juridical_person = row["法定代表人"]
            email_address = row["邮箱"]
            more_email_address = row["更多邮箱"].split(";") if len(row["更多邮箱"].strip()) > 1 else []
            if email_address not in more_email_address:
                more_email_address.append(email_address)
            excel_data.append({
                'company': company, 'juridical_person': juridical_person, "email_address_list": more_email_address,
            })
            # print(company, juridical_person, more_email_address)
            # if index+1 > 3:
            #     break
        return excel_data

    def send_finish_excel_read(self, file_path):
        """ 统计该邮箱地址 当前的发送次数 """
        send_count_dict = {}
        current_datetime = datetime.now().strftime('%Y-%m-%d')
        df = pd.read_excel(io=file_path, skiprows=0, usecols=None)
        for index, row in df.iterrows():
            email_address = row["发送人邮箱"]
            send_date = row["日期"]
            if send_date == current_datetime and row['状态'] == '发送成功':
                if email_address in send_count_dict:
                    send_count_dict[email_address] += 1
                else:
                    send_count_dict[email_address] = 1
        return send_count_dict

    def html_read(self, file_path):
        with open(file=file_path, mode='r', encoding='utf-8') as fis:
            content = fis.read()
        return content

    def img_read(self, file_path):
        with open(file=file_path, mode='rb') as fis:
            content = fis.read()
        return content

    def cookie_excel_read(self, file_path):
        df = pd.read_excel(io=file_path, skiprows=0, usecols=None)
        cookie_dict = dict()
        for index, row in df.iterrows():
            phone = row["手机号"]
            cookie = row["cookie"]
            cookie_dict[phone] = cookie
        return cookie_dict

    def email_excel_read(self, file_path):
        df = pd.read_excel(io=file_path, skiprows=0, usecols=None)
        email_dict = dict()
        for index, row in df.iterrows():
            address = row["发送人邮箱"]
            auth_code = row["授权码"]
            email_dict[address] = auth_code
        return email_dict

    def json_read(self, file_path):
        with open(file=file_path, mode='r', encoding='utf-8') as fis:
            json_data = fis.read()
        json_data = json.loads(json_data)
        return json_data


class DataSave(object):
    def __init__(self):
        pass

    def init_resource_file(self, directory_path):
        """ 创建目录 """
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

    def create_file(self, file_path, title_content):
        """ 创建文件 """
        self.init_resource_file(os.path.dirname(file_path))
        with open(file=file_path, mode='w', encoding='utf-8') as fis:
            fis.write(title_content)

    def csv_save(self, file_path, content):
        """ csv文件类型写入 """
        with open(file=file_path, mode='a', encoding='utf-8') as fis:
            fis.write(content)

    def csv_save_as_xlsx(self, file_path):
        """ 读取csv文件将结果写入xlsx """
        time.sleep(2)
        filename_prefix = os.path.splitext(file_path)[0]  # 切割文件路径以及后缀
        df = pd.read_csv(file_path, encoding='utf-8', dtype='object')
        df.to_excel(f"{filename_prefix}.xlsx", index=False)
        # print("csv 转 xlsx 成功!")

    def init_resource_file(self, directory_path):
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

    def json_save(self, file_path, setting_dict):
        self.init_resource_file(os.path.dirname(file_path))
        with open(file=file_path, mode='w', encoding='utf-8') as fis:
            fis.write(json.dumps(setting_dict, ensure_ascii=False, indent=4))

    def html_save(self, file_path, html_content):
        with open(file=file_path, mode="wb") as fis:
            fis.write(html_content)

# DataRead().qcc_excel_read()

