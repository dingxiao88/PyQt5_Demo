# -*- coding: utf-8 -*-

import sys
import psutil
import socket
import os
import struct
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QMouseEvent, QCursor

from ui_dx_new import *

# 从APP文件夹导入
from APP import APP_Fun
from APP import Menu_Fun
from Thread_Udp_Recv import Thread_Udp_Recv
from Thread_Udp_Send import Thread_Udp_Send

# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    # @1-全局量
    udpSocket = None
    udpSocket_send = None
    current_net_interface = None
    localIp = ""
    localPort = 0
    destIp = ""
    destPort = 0
    udp_connect_flag = False
    udp_send = []

    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        # 绑定窗口设置函数
        self.btn_close.clicked.connect(lambda:APP_Fun.APP_Close(main_win))
        self.btn_maximize_restore.clicked.connect(lambda:APP_Fun.APP_Max(main_win))
        self.btn_minimize.clicked.connect(lambda:APP_Fun.APP_Min(main_win))

        # 绑定设置menu显示
        self.btn_toggle_menu.clicked.connect((lambda: Menu_Fun.Show_Menu(self,200)))

        # 功能选项切换
        self.pushButton_dc_run.clicked.connect(lambda:Menu_Fun.Choose_Menu(self,1))
        self.pushButton_weather.clicked.connect(lambda:Menu_Fun.Choose_Menu(self,2))
        self.pushButton_config.clicked.connect(lambda:Menu_Fun.Choose_Menu(self,3))
        self.pushButton_about.clicked.connect(lambda:Menu_Fun.Choose_Menu(self,4))

        # 模式显示DC_Run界面
        self.stackedWidget.setCurrentIndex(0)

        # 初始化本地网卡
        self.Init_Local_Interface()
        self.comboBox_LocalInterface.currentIndexChanged.connect(self.On_interface_selection_change)
        # UDP连接
        self.pushButton_bing.clicked.connect(self.UDP_Connect)


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
            # self.udp_recv_thread.DX_Thread_OutSingal.connect(self.UDP_Recv_ShowInfo)
            self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send, self.destIp, self.destPort)
        
        else:
            self.udpSocket.close()
            # self.udpSocket_send.close()
            time.sleep(1)

    # --------UDP连接--------
    def UDP_Connect(self):
        if(self.udp_connect_flag == False):
            # 获取网络参数
            self.Get_IP_Port(6000)
            # 创建socket
            self.Set_Local_Socket(True)

        elif(self.udp_connect_flag == True):
            # 关闭socket
            self.Set_Local_Socket(False)

        # 获得线程运行的状态
        if(self.udp_recv_thread.working_flag == False):
            self.udp_recv_thread.setRun()
            self.udp_recv_thread.start()
            self.udp_connect_flag = True
            self.pushButton_bing.setText('断开')
            self.pushButton_setStyle(self.pushButton_bing, 1)

        elif(self.udp_recv_thread.working_flag == True):
            self.udp_recv_thread.setRun()
            self.udp_connect_flag = False
            self.pushButton_bing.setText('绑定')
            self.pushButton_setStyle(self.pushButton_bing, 0)

    
    # 按钮设置样式
    def pushButton_setStyle(self,which_pushButton,setFlag):
        if(setFlag == 1):
            which_pushButton.setStyleSheet('QPushButton {\
                                            color: rgb(234,237,237);\
                                            background-position: center;\
                                            background-repeat: no-reperat;\
                                            border: none;\
                                            background-color: rgb(85, 170, 255);\
                                            }')
        elif(setFlag == 0):
            which_pushButton.setStyleSheet('QPushButton {\
                                            color: rgb(234,237,237);\
                                            background-position: center;\
                                            background-repeat: no-reperat;\
                                            border: none;\
                                            background-color: rgb(27, 29, 35);\
                                            }\
                                            QPushButton:hover {\
                                            background-color: rgb(33, 37, 43);\
                                            }\
                                            QPushButton:pressed {	\
                                            background-color: rgb(85, 170, 255);\
                                            }')



    # 全局监听鼠标点击事件
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
    # 全局监听鼠标移动事件
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    # 全局监听鼠标释放事件
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

# 主入口
if __name__ == '__main__':
    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.setWindowTitle('霄哥的神秘工具V1.0')
    main_win.setWindowFlags(Qt.FramelessWindowHint)     # 无边框
    main_win.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
    main_win.show()
    sys.exit(app.exec_())