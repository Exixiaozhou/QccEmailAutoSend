import ssl
import smtplib
from datetime import datetime
from email.header import Header  # 构建邮件头
from email.mime.text import MIMEText  # email 用于构建邮件内容
from email.message import EmailMessage  # 消息对象
from email.mime.image import MIMEImage  # 图片对象
from email.mime.multipart import MIMEMultipart  # 文件对象
from common.setting import LocalResourcePath


smtp_server = "smtp.qq.com"  # 邮箱服务器
ssl_port = 465

authorization_code = 'tiwrfwvgsnyubbag'
email_address = '1725996866@qq.com'  # 发送方的邮箱

email_password = authorization_code
# receiver = ['2393175230@qq.com', '2892178330@qq.com', '2055427678@qq.com']  # 收件人邮箱
receiver = ['1348696457@qq.com']  # 收件人邮箱

msg = MIMEMultipart('mixed')  # 构造邮件对象MIMEMultipart

# 添加body
html_path = '../resource/html_template/test.html'
html_content = open(file=html_path, mode='r', encoding='utf-8').read()

msg.attach(MIMEText(html_content, 'html', 'utf-8'))  # plain代表纯文本,html代表支持html文本
# 主题、发件人、收件人、日期显示在邮件页面上
# msg['Subject'] = "企业不良记录消除中联建设集团股份有限公司"
# msg['From'] = email_address
# msg['TO'] = ','.join(receiver).replace(',', ';')
# msg['Date'] = datetime.now().strftime('%Y-%m-%d')

# 构造图片附件
# ico_path = '../resource/imgs/zhengshu.jpg'
# send_image_content = open(ico_path, 'rb').read()  # 打开文件，可以使用相对路劲和绝对路径
# image = MIMEImage(send_image_content)
# image.add_header('Content-ID', '<image1>')
# image["Content-Disposition"] = 'attachment; filename="小洲.jpg"'
# msg.attach(image)
#
# ico_path = '../resource/imgs/weifeng1.jpg'
# send_image_content = open(ico_path, 'rb').read()  # 打开文件，可以使用相对路劲和绝对路径
# image = MIMEImage(send_image_content)
# image.add_header('Content-ID', '<image2>')
# image["Content-Disposition"] = 'attachment; filename="小洲.jpg"'
# msg.attach(image)

def add_header_build(msg):
    # 主题、发件人、收件人、日期显示在邮件页面上
    msg['Subject'] = '企业不良记录消除中联建设集团股份有限公司'
    msg['From'] = email_address
    msg['TO'] = ','.join(receiver).replace(',', ';')
    msg['Date'] = datetime.now().strftime('%Y-%m-%d')
    return msg


def img_read(file_path):
    with open(file=file_path, mode='rb') as fis:
        content = fis.read()
    return content


def add_img_build(file_path, image_str, msg):
    """ 添加图片构造, 并显示在文本中 """
    send_image_content = img_read(file_path)
    image = MIMEImage(send_image_content)
    image.add_header('Content-ID', image_str)
    image["Content-Disposition"] = f'attachment; filename="{image_str}.jpg"'
    msg.attach(image)
    return msg


def img_build_controller(msg):
    # zs_img_path = '../resource/imgs/zhengshu.jpg'
    zs_img_path = LocalResourcePath.ZsImgPath.value
    image_str = '<image1>'
    msg = add_img_build(zs_img_path, image_str, msg)
    # wx_img_path = '../resource/imgs/weifeng1.jpg'
    wx_img_path = LocalResourcePath.WxIcoImgPath.value
    image_str = '<image2>'
    msg = add_img_build(wx_img_path, image_str, msg)
    return msg

msg = add_header_build(msg)
msg = img_build_controller(msg)
smtp = smtplib.SMTP_SSL(smtp_server, port=ssl_port)
smtp.login(email_address, email_password)  # 登录邮箱
smtp.sendmail(email_address, receiver, msg.as_string())  # 发送邮箱
smtp.quit()  # 退出发送
print('发送成功')

