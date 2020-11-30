#coding=utf-8

import requests

rep = requests.get('http://www.weather.com.cn/data/sk/101010500.html')
rep.encoding = 'utf-8'

print('返回:%s' %rep.json())
print('temp:%s' %rep.json()['weatherinfo']['temp'])