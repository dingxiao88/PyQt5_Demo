# -*- coding: utf-8 -*-

import socket
import sys
import time

port = 8001                             # 端口和上面一致
host = "192.168.41.6"                      # 服务器IP，这里服务器和客户端IP同一个  localhost
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.41.4", 8883))
for i in range(10):
    sock.sendto(b'Successful! Message %d! ' %i,(host, port))
    # sys.stdout.write("Script stdout --> \n")
    # sys.stdout.flush()
    # time.sleep(100)
    # sock.sendto(b'Successful! Message', (host, port))