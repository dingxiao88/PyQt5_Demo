#导入模块
import requests
from bs4 import BeautifulSoup
from lxml import etree
from requests_html import HTMLSession
import re
import json
from ast import literal_eval

# 建立一个会话（session）
session = HTMLSession()

#发送请求
url="https://ncov.dxy.cn/ncovh5/view/pneumonia"
# url="https://file1.dxycdn.com/2021/0701/164/7353667588540889843-135.json"  20210701请求头
#伪装请求头
headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
response = requests.get(url,timeout=30,headers=headers)
home_page = response.content.decode()


soup = BeautifulSoup(home_page, 'html.parser')
# print(soup.prettify())   打印html字符串
# print(type(soup))



# movie_containers = soup.find_all('div', class_ = 'root')   寻找html标签失败

script = soup.find('script', id = 'getStatisticsService')  #寻找script成功
# print(type(script))
# print(len(script))
# print(script)


rule = r'   try { window.getStatisticsService = {(.*?)}}catch' # 正则规则
slotList = re.findall(rule, script.text)
print(slotList)




# js: str = script.text.replace('\n', '')
# raw_json = re.search('<script id="getStatisticsService">try { window.getStatisticsService = \({.*}}catch\);', js, flags=re.MULTILINE)
# data = literal_eval(slotList)
# labels = data['id']
# print(raw_json)

# script = soup.find('script', {'id':'getPV'}).get_text()
# script = soup.find('script', {'id':'getStatisticsService'}).get_text()
# # print(type(soup.find('script', {'id':'getStatisticsService'}).get_text()))
# print(script)

# for script in soup.find_all('script'):
#     print(script.contents) 

# script = soup.find_all('script')[17]
# print(script.contents) 
