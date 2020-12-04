#coding=utf-8

from __future__ import unicode_literals
import requests
import json


# rep = requests.get('http://www.weather.com.cn/data/sk/101010500.html')
rep = requests.get('http://wthrcdn.etouch.cn/weather_mini?citykey=101010100')
rep.encoding = 'utf-8'


# print('返回:%s' %rep.json())
# print('temp:%s' %rep.json()['weatherinfo']['temp'])

str_x = rep.json()
# print(str_x)

js = json.loads(rep.text)
# print (json.dumps(js))
encoded_json = json.dumps(str_x, ensure_ascii=False)
print(encoded_json,type(encoded_json))