# -*- coding: utf-8 -*-


import requests
from clint.textui import progress

url = 'https://www.python.org/ftp/python/3.8.1/python-3.8.1-macosx10.9.pkg'

size = 0

try:
    res = requests.get(url, stream=True)
    total_length = int(res.headers.get('content-length'))
    print(total_length)

    with open("dx.bin", "wb") as pypkg:
        # for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1, width=100):
        for chunk in res.iter_content(chunk_size = 1024):
            if chunk:
                pypkg.write(chunk)
                size +=len(chunk)
                print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ total_length), float(size / total_length * 100)) ,end=' ')

except Exception as e:
    print('err---------->')

