# -*- coding: utf-8 -*-

import socket

port = 8001                             # 端口和上面一致
host = "localhost"                      # 服务器IP，这里服务器和客户端IP同一个
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(10):
    sock.sendto(b'Successful! Message %d! ' %i,(host, port))
    # sock.sendto(b'Successful! Message', (host, port))