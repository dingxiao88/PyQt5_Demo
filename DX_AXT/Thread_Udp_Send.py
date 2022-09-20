
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time

class Thread_Udp_Send(QThread):

    DX_Thread_OutSingal = pyqtSignal(str, int)

    # udp_send1-用于连续发送
    # udp_send2-用于点击发送
    def __init__(self, socket, udp_send1, udp_send2, send_ip, send_port,parent = None):
        super(Thread_Udp_Send, self).__init__(parent)
        self.working_flag = False
        self.oneShot = False
        self.Run_Count = 0
        self.socket = socket
        self.udp_send1 = udp_send1
        self.udp_send2 = udp_send2
        self.send_ip = send_ip
        self.send_port = send_port
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

    # 单次发送
    def setOneShot(self):
        self.oneShot = True

    # 线程运行主循环
    def run(self):
        self.Run_Count = self.Run_Count + 1
        if(self.Run_Count > 65000):
            self.Run_Count = 0
        # 模拟人机
        # self.udp_send[45] =  self.Run_Count//256
        # self.udp_send[46] =  self.Run_Count%256

        if(self.oneShot == True):
            self.oneShot = False
            data1 = bytes(self.udp_send2)
            self.socket.sendto(data1,(self.send_ip, self.send_port))
        else:
            while(self.working_flag == True):
                self.Run_Count = self.Run_Count + 1
                if(self.Run_Count > 65000):
                    self.Run_Count = 0
                # 模拟人机
                # self.udp_send[45] =  self.Run_Count//256
                # self.udp_send[46] =  self.Run_Count%256
                data2 = bytes(self.udp_send1)
                self.socket.sendto(data2,(self.send_ip, self.send_port))
                # 每秒50帧
                time.sleep(1) 
                # time.sleep(0.01) 
