# -*- coding: utf-8 -*-

import psutil
import socket
import os
import struct
import time
import datetime
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
        # self.destIp = "224.100.100.133"
        self.destIp = "192.168.0.19"
    # 获得远端Port------
    if(self.lineEdit_Remote_Port.text() == ''):
        # self.destPort = 21785
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
        # mreq = struct.pack('4sl', socket.inet_aton('224.100.100.133'), socket.INADDR_ANY)
        mreq = struct.pack('4sl', socket.inet_aton('224.100.23.200'), socket.INADDR_ANY)
        # mreq = struct.pack('4sl', socket.inet_aton('224.100.20.200'), socket.INADDR_ANY)
        self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        print("-----------MEMBERSHIP------------")
        # self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton('224.100.23.200') + socket.inet_aton('0.0.0.0'))

        # 创建thread
        self.udp_recv_thread = Thread_Udp_Recv(self.udpSocket)
        self.udp_recv_thread.DX_Thread_OutSingal.connect(self.AXT_Recv_Info_Display)
        # 模拟人机
        # self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send, self.destIp, self.destPort)
        # KW状态
        self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_KW_Status, self.udp_send_KW_ServoConfig, self.destIp, self.destPort)
        # KW随动配置
        # self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_KW_ServoConfig, self.destIp, self.destPort)
        # KW制止器控制
        # self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_KW_Stoper, self.destIp, self.destPort)
        # KW命令角度
        # self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_KW_Angel, self.destIp, self.destPort)

        #----------------------------------------------
        #AXT FK 状态询问报文
        # self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_AXT_FK_askStatus, self.udp_send_AXT_FK_askStatus, self.destIp, self.destPort)
        
    
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



#----------------------------------------AXT-------------------------------------------------------------

# AXT项目UDP发送数据-------------------
def UDP_AXT_Send(self, send_id):
    if(self.udp_connect_flag == True):
        # -获得当前时间
        date = datetime.date.today()
        time = datetime.datetime.now()
        # print(date.year)
        # print(date.month)
        # print(date.day)
        # print(time.hour)
        # print(time.minute)
        # print(time.second)
        
        # -年
        self.udp_send_AXT_FK_askStatus[5] = int(date.year % 256)
        self.udp_send_AXT_FK_askStatus[6] = int(date.year / 256)
        # -月
        self.udp_send_AXT_FK_askStatus[7] = date.month
        # -日
        self.udp_send_AXT_FK_askStatus[8] = date.day
        # -时
        self.udp_send_AXT_FK_askStatus[9] = time.hour
        # -分
        self.udp_send_AXT_FK_askStatus[10] = time.minute
        # -秒
        self.udp_send_AXT_FK_askStatus[11] = time.second

        # -发送状态询问报文
        if(send_id == 1):
            self.udp_axt_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_AXT_FK_askStatus, self.udp_send_AXT_FK_askStatus, self.destIp, self.destPort)
            if(self.udp_axt_send_thread.working_flag == False):
                self.udp_axt_send_thread.setOneShot()
                self.udp_axt_send_thread.start()

        # -发送装置控制报文
        elif(send_id == 2):
            # -装置控制报文数据打包 
            # 前盖控制-6~7bit保留 0-5bit:1~6号管前盖状态 0:关闭 1:打开
            self.udp_send_AXT_FK_ctlAXT[5] = (self.cmd_front_case1|(self.cmd_front_case2<<1)|(self.cmd_front_case3<<2)|(self.cmd_front_case4<<3)|(self.cmd_front_case5<<4)|(self.cmd_front_case6<<5)|(0<<6)|(0<<7))
            # 前盖有效
            self.udp_send_AXT_FK_ctlAXT[6] = 0x3f

            # 旋回角度
            # self.udp_send_AXT_FK_ctlAXT[7]
            # self.udp_send_AXT_FK_ctlAXT[8]
            # 俯仰角度
            # self.udp_send_AXT_FK_ctlAXT[9]
            # self.udp_send_AXT_FK_ctlAXT[10]

            # 备用
            self.udp_send_AXT_FK_ctlAXT[11] = 0x00
            self.udp_send_AXT_FK_ctlAXT[12] = 0x01

            self.udp_axt_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_AXT_FK_ctlAXT, self.udp_send_AXT_FK_ctlAXT, self.destIp, self.destPort)
            if(self.udp_axt_send_thread.working_flag == False):
                self.udp_axt_send_thread.setOneShot()
                self.udp_axt_send_thread.start()


        # -FS命令报文
        elif(send_id == 3):
            # 1~4#管FS命令
            self.udp_send_AXT_FK_cmdFS[5] = ((self.cmd_fs4 << 6) | (self.cmd_fs3 << 4) | (self.cmd_fs2 << 2) | (self.cmd_fs1))
            # 5~6#管FS命令
            self.udp_send_AXT_FK_cmdFS[6] = ((0 << 6) | (0 << 4) | (self.cmd_fs6 << 2) | (self.cmd_fs5))
            # FS命令有效
            self.udp_send_AXT_FK_cmdFS[7] = 0x3F 
            
            self.udp_axt_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_AXT_FK_cmdFS, self.udp_send_AXT_FK_cmdFS, self.destIp, self.destPort)
            if(self.udp_axt_send_thread.working_flag == False):
                    self.udp_axt_send_thread.setOneShot()
                    self.udp_axt_send_thread.start()


        # -气瓶压力设定报文
        elif(send_id == 4):
            self.udp_axt_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_AXT_FK_persureSet, self.udp_send_AXT_FK_persureSet, self.destIp, self.destPort)
            if(self.udp_axt_send_thread.working_flag == False):
                    self.udp_axt_send_thread.setOneShot()
                    self.udp_axt_send_thread.start()

        # -环境信息报文
        elif(send_id == 5):
            self.udp_axt_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send_AXT_FK_envInfo, self.udp_send_AXT_FK_envInfo, self.destIp, self.destPort)
            if(self.udp_axt_send_thread.working_flag == False):
                    self.udp_axt_send_thread.setOneShot()
                    self.udp_axt_send_thread.start()




# axt FS命令设定
def AXT_FS_Control(self):
    # -获得1#FS命令
    self.cmd_fs1 = self.comboBox_cmd_FS1.currentIndex()
    # print(self.cmd_fs1)

    # -获得2#FS命令
    self.cmd_fs2 = self.comboBox_cmd_FS2.currentIndex()

    # -获得3#FS命令
    self.cmd_fs3 = self.comboBox_cmd_FS3.currentIndex()

    # -获得4#FS命令
    self.cmd_fs4 = self.comboBox_cmd_FS4.currentIndex()

    # -获得5#FS命令
    self.cmd_fs5 = self.comboBox_cmd_FS5.currentIndex()

    # -获得6#FS命令
    self.cmd_fs6 = self.comboBox_cmd_FS6.currentIndex()
        
    UDP_AXT_Send(self, 3)


# axt 环境信息设定
def AXT_EnvironmentInfo_Set(self):

    # -获得设定的环境温度（开氏温度 0K=-273.0℃）
    if(self.lineEdit_cmd_environmentTemp.text() == ''):
        self.cmd_temperture = 20.0
    else:
        self.cmd_temperture = float(self.lineEdit_cmd_environmentTemp.text())
    
    # -输出开氏温度
    cmd_temperture_kaishi = self.cmd_temperture + 273
    self.label_environmentTemp_Info.setText('K='+ str(cmd_temperture_kaishi))
    cmd_temperture_kaishi = (cmd_temperture_kaishi * 10)

    # -获得海况设定
    self.cmd_seastate = self.comboBox_cmd_seaState.currentIndex()

    # -环境温度
    self.udp_send_AXT_FK_envInfo[5] = int(cmd_temperture_kaishi % 256)
    self.udp_send_AXT_FK_envInfo[6] = int(cmd_temperture_kaishi / 256)
    # -海况
    self.udp_send_AXT_FK_envInfo[7] = self.cmd_seastate

    UDP_AXT_Send(self, 5)

            
# axt 1至6气瓶压力设定
def AXT_Persure_Set(self):

    # -获得1#气瓶设定压力数值
    if(self.lineEdit_cmd_persureSet1.text() == ''):
        self.cmd_persure1 = 10.0
    else:
        temp_data = float(self.lineEdit_cmd_persureSet1.text())
        if(temp_data > 25):
            temp_data = 10.0
        self.cmd_persure1 = temp_data

    # -获得2#气瓶设定压力数值
    if(self.lineEdit_cmd_persureSet2.text() == ''):
        self.cmd_persure2 = 10.0
    else:
        temp_data = float(self.lineEdit_cmd_persureSet2.text())
        if(temp_data > 25):
            temp_data = 10.0
        self.cmd_persure2 = temp_data

    # -获得3#气瓶设定压力数值
    if(self.lineEdit_cmd_persureSet3.text() == ''):
        self.cmd_persure3 = 10.0
    else:
        temp_data = float(self.lineEdit_cmd_persureSet3.text())
        if(temp_data > 25):
            temp_data = 10.0
        self.cmd_persure3 = temp_data

    # -获得4#气瓶设定压力数值
    if(self.lineEdit_cmd_persureSet4.text() == ''):
        self.cmd_persure4 = 10.0
    else:
        temp_data = float(self.lineEdit_cmd_persureSet4.text())
        if(temp_data > 25):
            temp_data = 10.0
        self.cmd_persure4 = temp_data

    # -获得5#气瓶设定压力数值
    if(self.lineEdit_cmd_persureSet5.text() == ''):
        self.cmd_persure5 = 10.0
    else:
        temp_data = float(self.lineEdit_cmd_persureSet5.text())
        if(temp_data > 25):
            temp_data = 10.0
        self.cmd_persure5 = temp_data

    # -获得6#气瓶设定压力数值
    if(self.lineEdit_cmd_persureSet6.text() == ''):
        self.cmd_persure6 = 10.0
    else:
        temp_data = float(self.lineEdit_cmd_persureSet6.text())
        if(temp_data > 25):
            temp_data = 10.0
        self.cmd_persure6 = temp_data

    self.udp_send_AXT_FK_persureSet[5] = int(self.cmd_persure1 * 10)
    self.udp_send_AXT_FK_persureSet[6] = int(self.cmd_persure2 * 10)
    self.udp_send_AXT_FK_persureSet[7] = int(self.cmd_persure3 * 10)
    self.udp_send_AXT_FK_persureSet[8] = int(self.cmd_persure4 * 10)
    self.udp_send_AXT_FK_persureSet[9] = int(self.cmd_persure5 * 10)
    self.udp_send_AXT_FK_persureSet[10] = int(self.cmd_persure6 * 10)

    UDP_AXT_Send(self, 4)


# axt 俯仰/旋回角度控制
def AXT_FYXH_Angle_Control(self):

    # -获得命令旋回角度
    if(self.lineEdit_cmd_xh_angle.text() == ''):
        self.cmd_xh_angle = 0.0
    else:
        self.cmd_xh_angle = float(self.lineEdit_cmd_xh_angle.text())
    # -获得命令俯仰角度
    if(self.lineEdit_cmd_fy_angle.text() == ''):
        self.cmd_fy_angle = 0.0
    else:
        self.cmd_fy_angle = float(self.lineEdit_cmd_fy_angle.text())

    # 旋回角度(-120~120)
    if((self.cmd_xh_angle >= -120) and (self.cmd_xh_angle <= 120)):
        x = (abs(self.cmd_xh_angle) / 0.1)
        xx = int(x)
        # temp_bytes = struct.pack('f',x)
        temp_bytes = struct.pack('i',xx)
        B1 = temp_bytes[1]
        B0 = temp_bytes[0]
        if(self.cmd_xh_angle < 0):
            B1 = B1 | 0x80
        self.udp_send_AXT_FK_ctlAXT[7] = B1
        self.udp_send_AXT_FK_ctlAXT[8] = B0
        # print('0x%x'%self.udp_send_AXT_FK_ctlAXT[7])
        # print('0x%x'%self.udp_send_AXT_FK_ctlAXT[8])

        # 数据验算
        # data_181 = self.udp_send_AXT_FK_ctlAXT[7]
        # data_182 = self.udp_send_AXT_FK_ctlAXT[8]
        # data_flag = 0
        # if(data_181 >= 128):
        #     data_181 = data_181 & 0x7f
        #     data_flag = 1
        # temp_xh_angle = (data_181 * 256) + data_182
        # xh_angle = temp_xh_angle * 0.1
        # if(data_flag == 1):
        #     xh_angle = 0 - xh_angle
        # xh_angle = round(xh_angle, 2)
        # print(xh_angle)

    # # 俯仰角度(-20~0)
    if((self.cmd_fy_angle >= -20) and (self.cmd_fy_angle <= 0)):
        y = (abs(self.cmd_fy_angle) / 0.1)
        yy = int(y)
        # temp_bytes = struct.pack('f',y)
        temp_bytes = struct.pack('i',yy)
        B1 = temp_bytes[1]
        B0 = temp_bytes[0]
        if(self.cmd_fy_angle < 0):
            B1 = B1 | 0x80
        self.udp_send_AXT_FK_ctlAXT[9] = B1
        self.udp_send_AXT_FK_ctlAXT[10] = B0
        # print('0x%x'%self.udp_send_AXT_FK_ctlAXT[9])
        # print('0x%x'%self.udp_send_AXT_FK_ctlAXT[10])

        # 数据验算
        # data_181 = self.udp_send_AXT_FK_ctlAXT[9]
        # data_182 = self.udp_send_AXT_FK_ctlAXT[10]
        # data_flag = 0
        # if(data_181 >= 128):
        #     data_181 = data_181 & 0x7f
        #     data_flag = 1
        # temp_fy_angle = (data_181 * 256) + data_182
        # fy_angle = temp_fy_angle * 0.1
        # if(data_flag == 1):
        #     fy_angle = 0 - fy_angle
        # fy_angle = round(fy_angle, 2)
        # print(fy_angle)

    UDP_AXT_Send(self, 2)


# axt 1至6前盖控制
def AXT_FrontCast_Control(self, num):
    # print(num)

    # -1号管开/闭前盖
    if(num == 1):
        if(self.cmd_front_case1 == 0):
            self.cmd_front_case1 = 1
            self.pushButton_cmd_frontcase1.setText('1#关盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase1, 1)
        elif(self.cmd_front_case1 == 1):
            self.cmd_front_case1 = 0
            self.pushButton_cmd_frontcase1.setText('1#开盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase1, 0)

    # -2号管开/闭前盖
    elif(num == 2):
        if(self.cmd_front_case2 == 0):
            self.cmd_front_case2 = 1
            self.pushButton_cmd_frontcase2.setText('2#关盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase2, 1)
        elif(self.cmd_front_case2 == 1):
            self.cmd_front_case2 = 0
            self.pushButton_cmd_frontcase2.setText('2#开盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase2, 0)

    # -3号管开/闭前盖
    elif(num == 3):
        if(self.cmd_front_case3 == 0):
            self.cmd_front_case3 = 1
            self.pushButton_cmd_frontcase3.setText('3#关盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase3, 1)
        elif(self.cmd_front_case3 == 1):
            self.cmd_front_case3 = 0
            self.pushButton_cmd_frontcase3.setText('3#开盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase3, 0)

    # -4号管开/闭前盖
    elif(num == 4):
        if(self.cmd_front_case4 == 0):
            self.cmd_front_case4 = 1
            self.pushButton_cmd_frontcase4.setText('4#关盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase4, 1)
        elif(self.cmd_front_case4 == 1):
            self.cmd_front_case4 = 0
            self.pushButton_cmd_frontcase4.setText('4#开盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase4, 0)

    # -5号管开/闭前盖
    elif(num == 5):
        if(self.cmd_front_case5 == 0):
            self.cmd_front_case5 = 1
            self.pushButton_cmd_frontcase5.setText('5#关盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase5, 1)
        elif(self.cmd_front_case5 == 1):
            self.cmd_front_case5 = 0
            self.pushButton_cmd_frontcase5.setText('5#开盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase5, 0)

    # -6号管开/闭前盖
    elif(num == 6):
        if(self.cmd_front_case6 == 0):
            self.cmd_front_case6 = 1
            self.pushButton_cmd_frontcase6.setText('6#关盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase6, 1)
        elif(self.cmd_front_case6 == 1):
            self.cmd_front_case6 = 0
            self.pushButton_cmd_frontcase6.setText('6#开盖')
            Element_Style.pushButton_setStyle(self.pushButton_cmd_frontcase6, 0)

    UDP_AXT_Send(self, 2)


# axt 测试报文选择
def AXT_TestMsg_Send(self):
    self.AXT_Send_MesgID = self.comboBox_MesgID_Sel.currentIndex()
    # print(self.AXT_Send_MesgID)
    UDP_AXT_Send(self, (self.AXT_Send_MesgID + 1))