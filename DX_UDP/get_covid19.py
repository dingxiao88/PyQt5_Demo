#encoding:UTF-8
__author__ = 'DX'

#导入模块
import requests
from bs4 import BeautifulSoup
# from lxml import etree
# from requests_html import HTMLSession
import re
import json
# from ast import literal_eval
from PIL import Image

def get_Covid19_Data():
    # 建立一个会话（session）
    # session = HTMLSession()

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
    # print(soup)


    # movie_containers = soup.find_all('div', class_ = 'root')   寻找html标签失败

    script = soup.find('script', id = 'getStatisticsService')  #寻找script成功
    # print(type(script.text))
    # print(len(script))
    # print(script.string)

    test_txt = "<script id=\"getStatisticsService\">try { window.getStatisticsService = {123141231}}catch(e){}</script>"
    str = "<script id=\"getStatisticsService\">try { window.getStatisticsService = {123141231}"

    # rule = r"<script id=\"getStatisticsService\">try { window.getStatisticsService = {(.*)}}catch(e){}</script>" # 正则规则
    rule = r"{(.+)}"
    slotList = re.findall(rule, script.string)
    str1 = ''.join(slotList)
    # print(str1)
    # print(slotList)

    # rule1 = r"{(.+)"
    slotList1 = re.findall(rule, str1)
    # print(slotList1)

    rule1 = r"(.+)}"
    str2 = ''.join(slotList1)
    slotList2 = re.findall(rule1, str2)
    # print(slotList2)

    str3 = ''.join(slotList2)
    str_list = list(str3)    # 字符串转list
    str_list.insert(0, '{')
    str_list.insert((len(str_list)), '}')
    str_out = ''.join(str_list)    # 空字符连接
    # print(str_out)


    text = json.loads(str_out)
    print(text)
    # print(text['confirmedCount'])


# 在字符串指定位置插入字符
# str_origin：源字符串  pos：插入位置  str_add：待插入的字符串
#
def str_insert(str_origin, pos, str_add):
    str_list = list(str_origin)    # 字符串转list
    str_list.insert(pos, str_add)  # 在指定位置插入字符串
    str_out = ''.join(str_list)    # 空字符连接
    return  str_out



def get_zazhipdf_Data():

    #发送请求
    url="https://www.zazhipdf.com/"
    #伪装请求头
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    response = requests.get(url,timeout=30,headers=headers)
    response.encoding = 'gb2312'
    home_page = response.content.decode()

    soup = BeautifulSoup(home_page, 'html.parser')
    # print(soup.prettify())   #打印html字符串
    # print(type(soup))
    # print(soup)

    script = soup.find_all('div', class_  = 'placeholder')  
    # print(type(script.text))
    # print(len(script))
    # print(script.string)
    pdf1 = script[0]

    # print(pdf1.a.img)
    # print(pdf1.a.img['alt'])   #img标签alt属性
    # print(pdf1.a.img['data-src'])

    return pdf1

def img_png_to_jpg():

    image_url = "https://www.zazhipdf.com/wp-content/themes/rizhuti/timthumb.php?src=https://www.zazhipdf.com/wp-content/uploads/2021/07/da9ded8acca6cc1.png&h=270&w=270&zc=1&a=c&q=100&s=1"
    
    img_data = requests.get(image_url).content
    with open('/home/dx/sites/dx1023.com/django_blog/media/images/image_name1.png', 'wb') as handler:
        handler.write(img_data)

    im = Image.open('/home/dx/sites/dx1023.com/django_blog/media/images/image_name1.png')
    rgb_im = im.convert('RGB')
    rgb_im.save('/home/dx/sites/dx1023.com/django_blog/media/images/img_png_to_jpg.jpg')



get_Covid19_Data()

# pdf = get_zazhipdf_Data()
# # # print(pdf.a.img)
# print(pdf.a.img['alt'])   #img标签alt属性
# print(pdf.a.img['data-src'])

# img_png_to_jpg()
