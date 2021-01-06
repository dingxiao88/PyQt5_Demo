# -*- coding: utf-8 -*-

import psutil
import socket
import os
import struct
import time
from APP import Element_Style
from Thread_Udp_Recv import Thread_Udp_Recv
from Thread_Udp_Send import Thread_Udp_Send



# 初始化本地网卡-----
def Init_Local_Interface(self):
    
    self.comboBox_LocalInterface.clear()
    self.net_if = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()

    net_names = list(self.net_if.keys())

    for if_name in net_names:
        if not net_if_stats[if_name].isup:
            self.net_if.pop(if_name, None)
        else:
            self.comboBox_LocalInterface.addItem(if_name)
        
    current_interface = self.comboBox_LocalInterface.currentText()
    self.current_net_interface = current_interface

    for snicaddr in self.net_if[current_interface]:
        if snicaddr.family == socket.AF_INET:
            ipv4_add = snicaddr.address
            break
        else:
            ipv4_add = '0.0.0.0'
    
    self.label_InterfaceIP.setText(ipv4_add)
    self.lineEdit_Local_IP.setPlaceholderText(ipv4_add)
    self.localIp = ipv4_add
    print(ipv4_add)

# 本地网卡地址刷新--------------
def On_interface_selection_change(self):

    if(self.udp_connect_flag == False):
        current_interface = self.comboBox_LocalInterface.currentText()
        self.current_net_interface = current_interface

        if current_interface in self.net_if:
            for snicaddr in self.net_if[current_interface]:
                if snicaddr.family == socket.AF_INET:
                    ipv4_add = snicaddr.address
                    break
                else:
                    ipv4_add = '0.0.0.0'
        else:
            return

        self.label_InterfaceIP.setText(ipv4_add)
        self.lineEdit_Local_IP.setPlaceholderText(ipv4_add)
        self.localIp = ipv4_add

# 获取local和remot网络参数-------------
def Get_IP_Port(self, port):
    # # 获得本地IP---------
    # self.localIp = self.lineEdit_Local_IP.text()
    # if(self.localIp == ''):
    #     self.localIp = ip
    # 获得本地Port-----------
    if(self.lineEdit_Local_Port.text() == ''):
        self.localPort = port
    else:
        self.localPort = int(self.lineEdit_Local_Port.text())   

    # 获得远端IP------
    self.destIp = self.lineEdit_Remote_IP.text()
    if(self.destIp == ''):
        self.destIp = "224.100.23.200"
    # 获得远端Port------
    if(self.lineEdit_Remote_Port.text() == ''):
        self.destPort = 6000
    else:
        self.destPort = int(self.lineEdit_Remote_Port.text())  

# 配置Local Socket-----------------
def Set_Local_Socket(self, set_flag):
    if(set_flag == True):
        HOST = socket.gethostbyname(socket.gethostname())

        print("-----------net card------------"+HOST)
        print("-----------init ip-------------"+self.localIp)
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #非阻塞模式
        self.udpSocket.setblocking(False)
        # 超时
        self.udpSocket.settimeout(1)
        # # 绑定本地端口--可以使用该项区别组播和点播
        # self.udpSocket.bind((self.localIp,self.localPort))
        self.udpSocket.bind(('0.0.0.0',self.localPort))  
        # 声明该socket为多播类型
        self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) 
        # 加入组播地址
        mreq = struct.pack('4sl', socket.inet_aton('224.100.23.200'), socket.INADDR_ANY)
        self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        # self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton('224.100.23.200') + socket.inet_aton('0.0.0.0'))

        # 创建thread
        self.udp_recv_thread = Thread_Udp_Recv(self.udpSocket)
        self.udp_recv_thread.DX_Thread_OutSingal.connect(self.DC_Recv_Info_Display)
        self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send, self.destIp, self.destPort)
    
    else:
        self.udpSocket.close()
        # self.udpSocket_send.close()
        time.sleep(1)




# --------UDP连接--------
def UDP_Connect(self):
    if(self.udp_connect_flag == False):
        # 获取网络参数
        Get_IP_Port(self,6000)
        # 创建socket
        Set_Local_Socket(self,True)
        self.frame_size_grip.setStyleSheet('background: transparent;\
                                            background-image: url(:/images_icons_20/images/icons/20x20/cil-link.png);\
                                            background-position: center;\
                                            background-repeat: no-repeat;')
                                            

    elif(self.udp_connect_flag == True):
        # 关闭socket
        Set_Local_Socket(self,False)
        self.frame_size_grip.setStyleSheet('background: transparent;\
                                            background-image: url(:/images_icons_20/images/icons/20x20/cil-link-broken.png);\
                                            background-position: center;\
                                            background-repeat: no-repeat;')

    # 获得线程运行的状态
    if(self.udp_recv_thread.working_flag == False):
        self.udp_recv_thread.setRun()
        self.udp_recv_thread.start()
        self.udp_connect_flag = True
        self.pushButton_bing.setText('断开')
        Element_Style.pushButton_setStyle(self.pushButton_bing, 1)

    elif(self.udp_recv_thread.working_flag == True):
        self.udp_recv_thread.setRun()
        self.udp_connect_flag = False
        self.pushButton_bing.setText('绑定')
        Element_Style.pushButton_setStyle(self.pushButton_bing, 0)


# UDP连续发送--------------------------
def UDP_Send_Continue(self):
    if(self.udp_connect_flag == True):
        # 获得线程运行的状态
        if(self.udp_send_thread.working_flag == False):
            self.udp_send_thread.setRun()
            self.udp_send_thread.start()
            self.pushButton_udpSend_continue.setText('停止')
            Element_Style.pushButton_setStyle(self.pushButton_udpSend_continue, 1)

        elif(self.udp_send_thread.working_flag == True):
            self.udp_send_thread.setRun()
            self.pushButton_udpSend_continue.setText('连续发送')
            Element_Style.pushButton_setStyle(self.pushButton_udpSend_continue, 0)

# UDP单次发送--------------------------
def UDP_Send_Single(self):
    if(self.udp_connect_flag == True):
        if(self.udp_send_thread.working_flag == False):
            self.udp_send_thread.setOneShot()
            self.udp_send_thread.start()

