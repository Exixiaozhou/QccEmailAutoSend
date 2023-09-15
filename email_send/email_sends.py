import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText  # email 用于构建邮件内容
from email.message import EmailMessage  # 消息对象
from email.mime.image import MIMEImage  # 图片对象
from email.mime.multipart import MIMEMultipart  # 文件对象
from common.pipeline import DataRead


class QqEmailSend(object):
    def __init__(self):
        self.smtp_server = "smtp.qq.com"  # 邮箱服务器
        self.ssl_port = 465
        self.pipeline_read = DataRead()

    def add_header_build(self, params, msg):
        # 主题、发件人、收件人、日期显示在邮件页面上
        msg['Subject'] = f"企业不良记录消除{params['params']['company']}"
        msg['From'] = params['qq_account']['email_address']
        msg['TO'] = ','.join(params['params']['email_address_list']).replace(',', ';')
        msg['Date'] = datetime.now().strftime('%Y-%m-%d')
        return msg

    def add_body_build(self, html_content, msg):
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))  # plain代表纯文本,html代表支持html文本
        return msg

    def add_img_build(self, file_path, image_str, msg):
        """ 添加图片构造, 并显示在文本中 """
        send_image_content = self.pipeline_read.img_read(file_path)
        image = MIMEImage(send_image_content)
        image.add_header('Content-ID', image_str)
        image["Content-Disposition"] = f'attachment; filename="{image_str}.jpg"'
        msg.attach(image)
        return msg

    def add_file_build(self, file_path, msg):
        # 构造附件
        file_content = self.pipeline_read.img_read(file_path)
        text_att = MIMEText(file_content, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        # 重命名附件文件
        text_att.add_header('Content-Disposition', 'attachment', filename='requests_file_upload.txt')
        msg.attach(text_att)
        return msg

    def email_send(self, params, msg):
        # 发送邮件
        smtp = smtplib.SMTP_SSL(self.smtp_server, port=self.ssl_port)
        smtp.login(params['qq_account']['email_address'], params['qq_account']['authorization_code'])  # 登录邮箱
        # smtp.sendmail(params['qq_account']['email_address'], params['params']['email_address_list'], msg.as_string())
        address_list = params['params']['email_address_list']
        address_list += []  # 测试收件人邮箱
        smtp.sendmail(params['qq_account']['email_address'], address_list, msg.as_string())
        time.sleep(2)
        smtp.quit()  # 退出发送

    def create_msg_object(self):
        msg = MIMEMultipart('mixed')  # 构造邮件对象MIMEMultipart
        return msg
