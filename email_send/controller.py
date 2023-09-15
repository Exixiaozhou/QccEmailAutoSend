import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from common.pipeline import DataRead, DataSave
from common.setting import LocalResourcePath
from email_send.email_sends import QqEmailSend
from common.logger import Log


class QqEmailSendController(object):
    def __init__(self):
        self.email_send = QqEmailSend()
        self.pipeline_read = DataRead()
        self.pipeline_save = DataSave()
        self.logger = Log().get_logger()

    def update_html_content(self, params, file_path):
        html_content = self.pipeline_read.html_read(file_path)
        soup = BeautifulSoup(html_content, 'html.parser')  # 使用BeautifulSoup解析HTML文档
        soup.find(name='h3', id='fare').string = f"尊敬的{params['params']['juridical_person']}："
        soup.find(name='h3', id='company_name').string = f"{params['params']['company']}名下有："
        tip_dict = {
            'administrative_penalty': '条行政处罚记录', 'environmental_penalty': '条环保处罚记录',
            'history_break_faith': '条法院历史失信信息', 'history_consumption': '条法院历史限制高消费',
            'history_executor': '条法院历史被执行人',
        }
        for keys in params['company_data']:
            if keys not in tip_dict.keys():
                continue
            value = params['company_data'][keys]
            if int(value) < 1:
                soup.find(name='li', id=keys).extract()  # 删除某个标签
                continue
            soup.find(name='li', id=keys).string = f"{value}{tip_dict[keys]}"
        """ 新增标签，并将标签添加至某标签内 """
        img_div = soup.new_tag('div', id="img_div")  # 创建一个新的 <p>, 设置样式
        zs_img = soup.new_tag('img', src="cid:image1", id="zhengshu")  # 创建一个新的 <img> 标签并设置属性
        wx_img = soup.new_tag('img', src="cid:image2", id="WxQrCode")
        img_div.append(zs_img)  # 将 <img> 标签添加到 <p> 标签中
        img_div.append(wx_img)
        soup.find('div', class_='centered-div').append(img_div)  # 在body的div中添加标签
        company_name = soup.new_tag('p', attrs={'class': 'text_suffix'})
        company_name.string = '浙江泰禾泰企业管理咨询有限公司'
        soup.find('div', class_='centered-div').append(company_name)  # 在body的div中添加标签
        date_content = soup.new_tag('p', attrs={'class': 'text_suffix'})
        date_content.string = datetime.now().strftime('%Y-%m-%d')
        soup.find('div', class_='centered-div').append(date_content)  # 在body的div中添加标签
        html_content = soup.prettify("utf-8")
        return html_content

    def lastly_update_html(self, params, file_path):
        html_content = self.pipeline_read.html_read(file_path)
        soup = BeautifulSoup(html_content, 'html.parser')  # 使用BeautifulSoup解析HTML文档
        soup.find(name='h3', id='company_name').string = params['params']['company']
        """ 新增标签，并将标签添加至某标签内 """
        img_div = soup.new_tag('div', id="img_div")  # 创建一个新的 <p>, 设置样式
        zs_img = soup.new_tag('img', src="cid:image1", id="zhengshu")  # 创建一个新的 <img> 标签并设置属性
        wx_img = soup.new_tag('img', src="cid:image2", id="WxQrCode")
        img_div.append(zs_img)  # 将 <img> 标签添加到 <p> 标签中
        img_div.append(wx_img)
        soup.find('div', class_='centered-div').append(img_div)  # 在body的div中添加标签
        company_name = soup.new_tag('p', attrs={'class': 'text_suffix'})
        company_name.string = '浙江泰禾泰企业管理咨询有限公司'
        soup.find('div', class_='centered-div').append(company_name)  # 在body的div中添加标签
        date_content = soup.new_tag('p', attrs={'class': 'text_suffix'})
        date_content.string = datetime.now().strftime('%Y-%m-%d')
        soup.find('div', class_='centered-div').append(date_content)  # 在body的div中添加标签
        html_content = soup.prettify("utf-8")
        return html_content

    def body_build_controller(self, params, msg):
        html_path = LocalResourcePath.LastlyHtmlTemplatePath.value
        html_content = self.lastly_update_html(params, html_path)
        # html_content = self.update_html_content(params, html_path)
        # html_path = LocalResourcePath.TestHtmlTemplatePath.value
        # html_path ='../resource/html_template/test.html'
        # html_content = self.pipeline_read.html_read(html_path)
        save_file_path = LocalResourcePath.TestHtmlTemplatePath.value
        self.pipeline_save.html_save(save_file_path, html_content)
        msg = self.email_send.add_body_build(html_content, msg)
        return msg

    def img_build_controller(self, msg):
        zs_img_path = LocalResourcePath.ZsImgPath.value
        # zs_img_path = '../resource/imgs/zhengshu.jpg'
        image_str = '<image1>'
        msg = self.email_send.add_img_build(zs_img_path, image_str, msg)
        wx_img_path = LocalResourcePath.WxIcoImgPath.value
        # wx_img_path = '../resource/imgs/weifeng1.jpg'
        image_str = '<image2>'
        msg = self.email_send.add_img_build(wx_img_path, image_str, msg)
        return msg

    def file_build_controller(self, msg):
        file_path = LocalResourcePath.TestTxtFilePath.value
        msg = self.email_send.add_file_build(file_path, msg)
        return msg

    def get_logger_items(self, data, email_send_count_dict):
        params = data['params']
        company_data = data['company_data']
        qq_account = data['qq_account']
        logger_items = {
            'one': params['phone'], 'two':  params['company'], 'three': params['juridical_person'],
            'four': ','.join(params['email_address_list']).replace(',', ';'),
            'five': company_data['administrative_penalty'], 'six': company_data['environmental_penalty'],
            'seven': company_data['history_break_faith'], 'eight': company_data['history_consumption'],
            'nine': company_data['history_executor'], 'ten': qq_account['email_address'],
            'eleven': str(email_send_count_dict[qq_account['email_address']])
        }
        return logger_items

    def runs(self, params=None, email_send_count_dict=None):
        gui = params['params']['gui']
        qq_account = params['qq_account']
        logger_items = params['logger_items']
        logger_items['ten'] = qq_account['email_address']
        logger_items['eleven'] = str(email_send_count_dict[qq_account['email_address']])
        try:
            msg = self.email_send.create_msg_object()
            msg = self.email_send.add_header_build(params, msg)
            msg = self.body_build_controller(params, msg)
            msg = self.img_build_controller(msg)  # 问题所在
            # msg = self.file_build_controller(msg)
            self.email_send.email_send(params, msg)
            status = True
            status_content = "邮件-发送成功"
        except Exception:
            status = False
            status_content = "邮件-发送异常"
        logger_items['twelve'] = status_content
        self.logger.info(f"{params['params']['company']} {params['params']['juridical_person']} {status_content}")
        gui.gui_log_object.email_log_output(gui.ui.emailSendTableWidget, logger_items)
        time.sleep(random.randint(10, 20))
        return status


# QqEmailSendController().runs()
