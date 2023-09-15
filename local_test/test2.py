import ssl
import smtplib
from email.header import Header  # 构建邮件头
from email.mime.text import MIMEText  # email 用于构建邮件内容
from email.message import EmailMessage  # 消息对象
from email.mime.image import MIMEImage  # 图片对象
from email.mime.multipart import MIMEMultipart  # 文件对象


# html_content = '''
#     <p>和田地区昌龙房地产开发有限责任公司</p>
#     <p><img src="cid:image1"></p>
#     <p>【2023-06-14】30条历史被执行人，新疆维吾尔自治区和田地区和田市人民法院的被执行人记录，目前公示在“ 企查查”等第三方大数据平台上。</p>
#     <p>【这条被执行人记录影响到了贵司的企业招投标、融资信贷、资质认定意向客户合作和公司信誉，更影响企业发展】</p>
#     <p>贵司符合条件，现可以免费申请撤销历史被执行人的公示。</p>
#     <p>服务单位：国有控股企业--浙江泰禾泰企业管理咨询有限公司</p>
#     <p>联系人：曾老师19012822250</p>
#     <p><img src="cid:image2"></p>
#     '''
html_path = '../resource/html_template/test.html'
html_content = open(file=html_path, mode='r', encoding='utf-8').read()

smtp_server = "smtp.qq.com"  # 邮箱服务器
ssl_port = 465
# authorization_code = 'immtadzkvmyhcbjb'
# email_address = '2053216453@qq.com'  # 发送方的邮箱

authorization_code = 'vwldxhlszqrgbidf'
email_address = '2055427678@qq.com'  # 发送方的邮箱

email_password = authorization_code
receiver = ['2393175230@qq.com', '2892178330@qq.com']  # 收件人邮箱

msg = MIMEMultipart('mixed')  # 构造邮件对象MIMEMultipart
msg.attach(MIMEText(html_content, 'html', 'utf-8'))  # plain代表纯文本,html代表支持html文本
# 主题、发件人、收件人、日期显示在邮件页面上
msg['Subject'] = "企业不良记录消除中联建设集团股份有限公司"
msg['From'] = email_address
msg['TO'] = ";".join(receiver)
msg['Date'] = '2022.11.10'

# 2393175230@qq.com	oinjhgcdsgshdjag
# 3082160195@qq.com	vfoqchdtgpncdfca
# 2055427678@qq.com	vwldxhlszqrgbidf
# 1725996866@qq.com	tiwrfwvgsnyubbag


# 构造文字内容
# body = """
#     和田地区昌龙房地产开发有限责任公司
#     【2023-06-14】30条历史被执行人，新疆维吾尔自治区和田地区和田市人民法院的被执行人记录，目前公示在“ 企查查”等第三方大数据平台上。
#     【这条被执行人记录影响到了贵司的企业招投标、融资信贷、资质认定意向客户合作和公司信誉，更影响企业发展】
#     贵司符合条件，现可以免费申请撤销历史被执行人的公示。
#     服务单位：国有控股企业--浙江泰禾泰企业管理咨询有限公司
#     联系人：曾老师19012822250
#     """
# text_plain = MIMEText(body, 'plain', 'utf-8')
# msg.attach(text_plain)

# 构造图片附件
ico_path = '../resource/imgs/zhengshu.jpg'
send_image_content = open(ico_path, 'rb').read()  # 打开文件，可以使用相对路劲和绝对路径
image = MIMEImage(send_image_content)
image.add_header('Content-ID', '<image1>')
image["Content-Disposition"] = 'attachment; filename="小洲.jpg"'
msg.attach(image)

ico_path = '../resource/imgs/weifeng1.jpg'
send_image_content = open(ico_path, 'rb').read()  # 打开文件，可以使用相对路劲和绝对路径
image = MIMEImage(send_image_content)
image.add_header('Content-ID', '<image2>')
image["Content-Disposition"] = 'attachment; filename="小洲.jpg"'
msg.attach(image)


# 构造附件
# file_path = 'resource/data/request_file_upload.txt'
# send_file = open(file_path, 'rb').read()
# text_att = MIMEText(send_file, 'base64', 'utf-8')
# text_att["Content-Type"] = 'application/octet-stream'
# # 重命名附件文件
# text_att.add_header('Content-Disposition', 'attachment', filename='requests_file_upload.txt')
# msg.attach(text_att)

# 发送邮件
smtp = smtplib.SMTP_SSL(smtp_server, port=ssl_port)
# smtp = smtplib.SMTP()  # 邮箱对象
# smtp.connect(smtp_server, 25)
smtp.login(email_address, email_password)  # 登录邮箱
smtp.sendmail(email_address, receiver, msg.as_string())  # 发送邮箱
smtp.quit()  # 退出发送
print('发送成功')
