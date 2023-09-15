import re
import requests

"""
    1、行政处罚
    2、环保处罚
    3、历史失信信息
    4、历史限制高消费
    5、历史被执行人
    
    企查查：https://www.qcc.com/
    13357122135
    19012822655
    19012822250
    密码：333666feng

    爱企查：https://aiqicha.baidu.com/
"""

headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'cookie': 'QCCSESSID=3eaf1b9c594c6668ff7f933b3e;',
    # 'cookie': 'QCCSESSID=db6ea6b9294530fcf2131d742c;',
    # 'cookie': 'QCCSESSID=f1199320b1674f864f71d8d3e7;',
    # 'cookie': 'QCCSESSID=bae6bacc2e547ffa1d898f6d4a;',
    # 'cookie': 'QCCSESSID=99529107239b4971aaa7c7bf1f;',
    # 'cookie': 'QCCSESSID=863560d59f6f3d44c590d71f00;',
    # 'cookie': 'QCCSESSID=da1c28f62f4ee3c0ec49d5c622;',
    'cookie': 'QCCSESSID=fda34a9e66ef9a2acb00cab351;',
    # 'cookie': 'acw_tc=75a76ba016910586309435293e7b7918a9cec43d45561cc6b526a54c59; QCCSESSID=62353bc4e4f7ad226d41433d91; qcc_did=51b2c886-6cd8-4c79-8059-31a0352ae258',
    # qcc_did=c922aa5d-969b-4cce-914f-f15532fd3f26; acw_tc=75a76bad16904464432164490ec169054d1e0e881087b84e75509a3e0f
    # acw_tc=701dd39716904687070058329e28445f69ec4f28f6e8d500b70d56949f
    # 'cookie': 'QCCSESSID=db75fac6f144969aaf4954c180; qcc_did=b1784f29-a0de-415f-8bac-3956cb62f120; acw_tc=701dd39716904687070058329e28445f69ec4f28f6e8d500b70d56949f',
    # 'acw_tc=75a8960716905080309566078ec922a507d77527234ff685592cfe4e97; QCCSESSID=f70bbc91c43878b303c17bf319; qcc_did=03e0ec60-7604-4c5f-bf22-5ddaadb33d85'
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

keyword = '宏恒建设有限公司'
juridical_person = '凌海亮'
index_url = f'https://www.qcc.com/web/search?key={keyword}'
response = requests.get(url=index_url, headers=headers)
# print(response.text)
html_string = response.text

url_code_list = re.findall(pattern='https://www.qcc.com/firm/(.*?).html', string=html_string)
url_list = list()
for code in url_code_list:
    url = f"https://www.qcc.com/firm/{code}.html"
    if len(url) != 62 or url in url_list:
        continue
    url_list.append(url)
print(len(url_list), url_list)

for url in url_list:
    response = requests.get(url=url, headers=headers)
    html_string = response.text
    if keyword not in html_string or juridical_person not in html_string:
        continue
    # print(html_string)
    administrative_penalty = re.search(pattern='"行政处罚".*?"count":(.*?),', string=html_string)
    environmental_penalty = re.search(pattern='"环保处罚".*?"count":(.*?),', string=html_string)
    history_break_faith = re.search(pattern='"历史失信信息".*?"count":(.*?),', string=html_string)
    history_consumption = re.search(pattern='"历史限制高消费".*?"count":(.*?),', string=html_string)
    history_executor = re.search(pattern='"历史被执行人".*?"count":(.*?),', string=html_string)
    print("行政处罚", administrative_penalty.group(1))
    print("环保处罚", environmental_penalty.group(1))
    print("历史失信信息", history_break_faith.group(1))
    print("历史限制高消费", history_consumption.group(1))
    print("历史被执行人", history_executor.group(1))
    break


