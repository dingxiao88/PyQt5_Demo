
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import struct

class Thread_Udp_Recv(QThread):

    DX_Thread_OutSingal = pyqtSignal(str, int)

    def __init__(self, socket, parent = None):
        super(Thread_Udp_Recv, self).__init__(parent)
        self.working_flag = False
        self.Run_Count = 0
        self.socket = socket
        # print('thread init')


    # 线程运行控制
    def setRun(self):
        if(self.working_flag == False):
            self.working_flag = True
            self.DX_Thread_OutSingal.emit('thread set run', 1)

        elif(self.working_flag == True):
            self.working_flag = False
            self.Run_Count = 0
            self.DX_Thread_OutSingal.emit('thread set stop', 0)


    # 线程运行主循环
    def run(self):
        while(self.working_flag == True):
            try:
                # receiveData = udpSocket.recvfrom(1024)
                recv_msg, recv_addr = self.socket.recvfrom(1024)
                # print("<<%s:%s"%(str(receiveData[1]),str(receiveData[0])))
                # print("<<"+str(recv_addr[0]))
                # if(str(recv_addr[0]) == "192.168.0.106"):
                if(str(recv_addr[0]) == "10.0.0.18"):

                    # msg1 = struct.unpack('!50B',recv_msg)  #!网络字节顺序 20字节 B unsigned char
                    # print(msg1[5])

                    # print("yes")
                    self.Run_Count = self.Run_Count + 1
                    send_str = 'send count:{0}'.format(self.Run_Count)
                    self.DX_Thread_OutSingal.emit(send_str, self.Run_Count)
                    # # print("<<"+str(recv_addr[0]))
                    # print(udp_recv_count)
                time.sleep(0.01) 
            except Exception as e:
                pass