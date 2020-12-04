# coding=utf-8

import json



m = {'a' : '你好'}

print (m)


print (json.dumps(m))


print (json.dumps(m,ensure_ascii=False))


# print (json.dumps(m,ensure_ascii=False).decode('utf8').encode('gb2312'))
