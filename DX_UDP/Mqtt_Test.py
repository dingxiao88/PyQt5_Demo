
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import os,base64 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    print("topic:"+msg.topic)
    # imgdata = base64.b64decode(str(msg.payload))
    # imgdata = base64.b64decode(f.read())
    file = open('1.jpg','wb')
    file.write(msg.payload)
    file.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('47.98.157.233', 8881, 100) # 600为keepalive的时间间隔
client.subscribe('pic', qos=0)
client.loop_forever() # 保持连接
