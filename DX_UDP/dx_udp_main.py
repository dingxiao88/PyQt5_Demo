
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 天气API参考：https://zhuanlan.zhihu.com/p/60815507

import sys
import socket
import os
import requests
import json
import threading
import struct
import time
import psutil
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QAction, QMenu)
# from PyQt5.QtGui import QRegExpValidator, QIcon, QPixmap, QColor
# from PyQt5.QtCore import pyqtSignal, Qt, QRegExp

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Thread_Main import DX_Thread
from Thread_Udp_Recv import Thread_Udp_Recv
from Thread_Udp_Send import Thread_Udp_Send
from dx_SystemTray import dx_SystemTray

# ui_main.py中内容
from ui_main import *


# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    # @1-创建udp连接信号
    # ConnectSignal = pyqtSignal(bool)
    # UDP_Recv_Signal = pyqtSignal(int)

    # @2-全局量
    udpSocket = None
    tr = None
    localIp = ""
    localPort = 0
    destIp = ""
    destPort = 0
    udp_recv_count = 0
    udp_send_count = 0
    udp_connect_flag = False
    udp_send = []
    recv_msg = ()
    recv_addr = ()
    

    def __init__(self, parent=None):

        # UDP组播发送-----------------------------
        # self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # #非阻塞模式
        # self.udpSocket.setblocking(False)
        # # 超时
        # self.udpSocket.settimeout(1)
        # # # 绑定本地端口
        # # self.udpSocket.bind(("192.168.31.188",6000))
        # #告诉内核这是一个多播类型的socket
        # self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) 
        # # 加入组播地址
        # mreq = struct.pack('4sl', socket.inet_aton('224.100.23.200'), socket.INADDR_ANY)
        # self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # 创建UDP收发线程
        # tr = threading.Thread(target = lambda:self.udp_receiveInfo(udpSocket))
        # tr.setDaemon(True)  #设置为后台线程
        # tr.setName("th-udp recv")
        # ts = threading.Thread(target = udp_sendInfo)

        # tr.start()
        # # ts.start()

        # tr.join()
        # ts.join()

        # self.Set_Local_Socket("192.168.0.107")

        # --------------------------------------------------------------
        # 关闭所有窗口,也不关闭应用程序
        # QApplication.setQuitOnLastWindowClosed(False)
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        # 创建UDP发送数据
        self.udp_send = []
        for x in range(50):
            self.udp_send.append(0x00)

        # @2-创建udp连接标志量
        self.UDP_Connect_Flag = False
        # @3-天气城市id
        self.Weather_ID = '101210101'  #默认是杭州

        # @4-UDP 收发线程-----------------------------
        # self.udp_recv_thread = Thread_Udp_Recv(self.udpSocket)
        # self.udp_recv_thread.DX_Thread_OutSingal.connect(self.UDP_Recv_ShowInfo)
        # self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send)
        
        # 软件状态栏显示
        self.statusBar().showMessage('reday.')

        # 显示软件图标  -- 运行python命令的目录必须在文件目录，不然会报错
        # path = os.path.abspath('.')
        # image_path = path + '\me.png'
        # print(image_path)
        self.setWindowIcon(QIcon("./images/me.png"))
        # self.setWindowIcon(QIcon(image_path))

        # 初始化本地网卡
        self.Init_Local_Interface()
        self.comboBox_LocalInterface.currentIndexChanged.connect(self.on_interface_selection_change)

        # 配置系统托盘
        # dx_SystemTray.setTary(self)
        self.dx_SystemTray1 = dx_SystemTray()
        self.dx_SystemTray1.dx_SystemTray_Signal.connect(self.SystemTray_Pro)

        # 安装正则表达式输入验证器
        rx = QtCore.QRegExp("\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b")
        self.lineEdit_Local_IP.setValidator(QRegExpValidator(rx,self))
        # self.lineEdit_Local_IP.setInputMask("000.000.000.000;_")

        # 天气查询按键绑定点击触发信号
        self.pushButton_Weather_Check.clicked.connect(self.Weather_Check)

        # 绑定按钮增加样式
        self.pushButton_bing.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')

        # 按钮绑定触发事件-----------------
        # UDP连接
        # self.pushButton_bing.clicked.connect(lambda:self.UDP_Connect(tr))
        self.pushButton_bing.clicked.connect(self.UDP_Connect)
        # # UDP单击发送
        self.pushButton_udpSend.clicked.connect(self.UDP_Send_Single)
        # UDP连续发送
        self.pushButton_udpSend_continue.clicked.connect(self.UDP_Send_Continue)
        self.pushButton_udpSend_continue.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
    
        # 获得本地IP---for PC
        # self.hostname = socket.gethostname()
        # self.ip = socket.gethostbyname(self.hostname)
        # # 获得本地IP---for PI4
        # # gw = os.popen("ip -4 route show default").read().split()
        # # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # # s.connect((gw[2], 0))
        # # self.ip = s.getsockname()[0]
        # print(self.ip)
        # self.lineEdit_Local_IP.setPlaceholderText(self.ip)

        # 线程启动按钮绑定事件------------
        self.dx_thread = DX_Thread("dx")
        self.dx_thread.DX_Thread_OutSingal.connect(self.Thread_Info)
        self.pushButton_thread_start.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        self.pushButton_thread_start.clicked.connect(self.Thread_Run)

        #--------------------------DC 控制-----------------------------------
        self.DC_FY_CmdRun = False
        self.DC_XH_CmdRun = False

        self.pushButton_DC_FYRunCtl.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        self.pushButton_DC_XHRunCtl.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')

        self.pushButton_DC_FYRun_Up.setIcon(QIcon(QPixmap('./images/up.png')))
        self.pushButton_DC_FYRun_Down.setIcon(QIcon(QPixmap('./images/down.png')))
        self.pushButton_DC_XHRun_Left.setIcon(QIcon(QPixmap('./images/left.png')))
        self.pushButton_DC_XHRun_Right.setIcon(QIcon(QPixmap('./images/right.png')))

        self.pushButton_DC_FYRun_Up.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
        self.pushButton_DC_FYRun_Down.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
        self.pushButton_DC_XHRun_Left.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
        self.pushButton_DC_XHRun_Right.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')

        # 绑定信号
        self.pushButton_DC_FYRunCtl.clicked.connect(self.DC_FYRun)
        self.pushButton_DC_XHRunCtl.clicked.connect(self.DC_XHRun)

        self.pushButton_DC_FYRun_Up.pressed.connect(self.DC_FYRun1)
        self.pushButton_DC_FYRun_Up.released.connect(self.DC_FYRun2)
        self.pushButton_DC_FYRun_Down.pressed.connect(self.DC_FYRun3)
        self.pushButton_DC_FYRun_Down.released.connect(self.DC_FYRun4)

        self.pushButton_DC_XHRun_Left.pressed.connect(self.DC_XHRun1)
        self.pushButton_DC_XHRun_Left.released.connect(self.DC_XHRun2)
        self.pushButton_DC_XHRun_Right.pressed.connect(self.DC_XHRun3)
        self.pushButton_DC_XHRun_Right.released.connect(self.DC_XHRun4)

        #--------------------------DC 反馈信息--------------------------------------------------------------
        self.DC_Dev_Status = 1      #随动设备状态 0：正常   1：不明   2：关机   3：故障
        self.DC_FY_RunStatus = 2    #FY运行状态 0：停止   1：运行   2：未知
        self.DC_XH_RunStatus = 2    #XH运行状态 0：停止   1：运行   2：未知

        if(self.DC_Dev_Status == 0):
            self.label_DC_Dev_Status.setStyleSheet('QLabel {background-color: #16A951; color: black;}')  #绿
        elif(self.DC_Dev_Status == 1):
            self.label_DC_Dev_Status.setStyleSheet('QLabel {background-color: #F0C239; color: black;}')  #黄
        elif(self.DC_Dev_Status == 2):
            self.label_DC_Dev_Status.setStyleSheet('QLabel {background-color: #FFF2DF; color: black;}')  #白
        elif(self.DC_Dev_Status == 3):
            self.label_DC_Dev_Status.setStyleSheet('QLabel {background-color: #F20C00; color: black;}')  #红

        if(self.DC_FY_RunStatus == 0):
            self.label_DC_FYStatus.setStyleSheet('QLabel {background-color: #F20C00; color: black;}')  #红
        elif(self.DC_FY_RunStatus == 1):
            self.label_DC_FYStatus.setStyleSheet('QLabel {background-color: #16A951; color: black;}')  #绿
        elif(self.DC_FY_RunStatus == 2):
            self.label_DC_FYStatus.setStyleSheet('QLabel {background-color: #F0C239; color: black;}')  #黄

        if(self.DC_XH_RunStatus == 0):
            self.label_DC_XHStatus.setStyleSheet('QLabel {background-color: #F20C00; color: black;}')  #红
        elif(self.DC_XH_RunStatus == 1):
            self.label_DC_XHStatus.setStyleSheet('QLabel {background-color: #16A951; color: black;}')  #绿
        elif(self.DC_XH_RunStatus == 2):
            self.label_DC_XHStatus.setStyleSheet('QLabel {background-color: #F0C239; color: black;}')  #黄

        self.label_DC_XHAngel.setText('5.99')
        self.label_DC_XHAngel.setText('-129.23')

        # 显示界面
        self.show()

    # 配置Local Socket-----------------
    def Set_Local_Socket(self, set_flag):
        if(set_flag == True):
            print("-----------init ip-------------"+self.localIp)
            self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #非阻塞模式
            self.udpSocket.setblocking(False)
            # 超时
            self.udpSocket.settimeout(1)
            # # 绑定本地端口
            self.udpSocket.bind((self.localIp,self.localPort))
            #告诉内核这是一个多播类型的socket
            self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) 
            # 加入组播地址
            mreq = struct.pack('4sl', socket.inet_aton('224.100.23.200'), socket.INADDR_ANY)
            self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            # 创建thread
            self.udp_recv_thread = Thread_Udp_Recv(self.udpSocket)
            self.udp_recv_thread.DX_Thread_OutSingal.connect(self.UDP_Recv_ShowInfo)
            self.udp_send_thread = Thread_Udp_Send(self.udpSocket, self.udp_send, self.destIp, self.destPort)
        else:
            self.udpSocket.close()
            time.sleep(1)


    # 本地网卡地址刷新--------------
    def on_interface_selection_change(self):
        if(self.udp_connect_flag == False):
            current_interface = self.comboBox_LocalInterface.currentText()

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


    # FY运行控制--------------------------
    def DC_FYRun(self):
        if(self.DC_FY_CmdRun == False):
            self.DC_FY_CmdRun = True
            self.pushButton_DC_FYRunCtl.setText("停止")
            self.pushButton_DC_FYRunCtl.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
            self.udp_send[3] = 1  #FY运行
            print("FY-Run")
        else:
            self.DC_FY_CmdRun = False
            self.pushButton_DC_FYRunCtl.setText("启动")
            self.pushButton_DC_FYRunCtl.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
            self.udp_send[3] = 0  #FY停止
            print("FY-Stop")

    def DC_FYRun1(self):
        # if(self.DC_FY_RunStatus == 1):
        self.pushButton_DC_FYRun_Up.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        self.udp_send[0] = 54
        print("FY-up")
    def DC_FYRun2(self):
        # if(self.DC_FY_RunStatus == 1):
        self.pushButton_DC_FYRun_Up.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
        self.udp_send[0] = 0
        print("FY-none")
    def DC_FYRun3(self):
        # if(self.DC_FY_RunStatus == 1):
        self.pushButton_DC_FYRun_Down.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        self.udp_send[0] = 51
        print("FY-down")
    def DC_FYRun4(self):
        # if(self.DC_FY_RunStatus == 1):
        self.pushButton_DC_FYRun_Down.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
        self.udp_send[0] = 0
        print("FY-none")

    # XH运行控制------------------
    def DC_XHRun(self):
        if(self.DC_XH_CmdRun == False):
            self.DC_XH_CmdRun = True
            self.pushButton_DC_XHRunCtl.setText("停止")
            self.pushButton_DC_XHRunCtl.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
            self.udp_send[4] = 1  #XH运行
            print("XH-Run")
        else:
            self.DC_XH_CmdRun = False
            self.pushButton_DC_XHRunCtl.setText("启动")
            self.pushButton_DC_XHRunCtl.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
            self.udp_send[4] = 0  #XH停止
            print("XH-Stop")

    def DC_XHRun1(self):
        # if(self.DC_XH_RunStatus == 1):
        self.pushButton_DC_XHRun_Left.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        self.udp_send[0] = 38
        print("XH-left")
    def DC_XHRun2(self):
        # if(self.DC_XH_RunStatus == 1):
        self.pushButton_DC_XHRun_Left.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
        self.udp_send[0] = 0
        print("XH-none")
    def DC_XHRun3(self):
        # if(self.DC_XH_RunStatus == 1):
        self.pushButton_DC_XHRun_Right.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        self.udp_send[0] = 53
        print("XH-right")
    def DC_XHRun4(self):
        # if(self.DC_XH_RunStatus == 1):
        self.pushButton_DC_XHRun_Right.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
        self.udp_send[0] = 0
        print("XH-none")



    # 主程序全局关闭事件监听
    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    # QSystemTrayIcon.NoIcon
    # QSystemTrayIcon.Information
    # QSystemTrayIcon.Warning
    # QSystemTrayIcon.Critical
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.dx_SystemTray1.showMsg(1, "程序缩小至系统托盘!")


    # 系统托盘类信号数据处理
    def SystemTray_Pro(self,str_info):
        if(str_info == "show"):
            self.showApp_dx()
        elif(str_info == "close"):
            self.closeApp_dx()


    # 关闭程序
    def closeApp_dx(self):
        # 点击关闭按钮或者点击退出事件会出现图标无法消失的bug，需要手动将图标内存清除
        sys.exit(app.exec_())

    # 显示程序
    def showApp_dx(self):
        self.show()

    # 启停线程
    def Thread_Run(self):
        # 获得线程运行的状态
        if(self.dx_thread.working_flag == False):
            self.dx_thread.setRun()
            self.dx_thread.start()
            self.pushButton_thread_start.setText('停止')
            self.pushButton_thread_start.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')

        elif(self.dx_thread.working_flag == True):
            self.dx_thread.setRun()
            self.pushButton_thread_start.setText('启动')
            self.pushButton_thread_start.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        

    # 线程信息打印
    def Thread_Info(self, str_info, count):
        self.textEdit_thread.setText(str_info)
        if(count == 10000):
            self.dx_SystemTray1.showMsg(1, "已成功发送10000次!")


    # --------城市查询------------
    def City_Check(self):
        # 获得城市id标志
        get_city = False
        # 获得城市名字
        city_name = self.lineEdit_Weather_City.text()
        # print(city_name)
        if(city_name == ''):
            city_name = '杭州'

        path = os.path.abspath('.')
        fn = path + '\weather_city_id.txt'
        # print(fn)
        file = open(fn,'r',encoding='utf-8',errors='ignore')
        line = file.readline()
        while line:
            line = file.readline()        #读取一行
            txt1 = line.encode("utf-8")   #编码成utf-8格式
            txt2 = txt1.decode("utf-8")   #解码成utf-8格式
            # print(txt2)
            txt3 = txt2.split(',')              #字符窜数据按‘，’拆分
            txt_city_name = txt3[0]
            if(city_name == txt_city_name):
                if(len(txt3) > 0):
                    txt4 = txt3[1].split('\n')
                    # print(txt4)
                    self.Weather_ID = txt4[0]
                    self.statusBar().showMessage('find city id.')
                    get_city = True
                    # print(self.Weather_ID) 
                    break
        file.close()
        return get_city


    # --------天气查询------------
    def Weather_Check(self):

        res = self.City_Check()

        if(res == True):
            rep = requests.get('http://wthrcdn.etouch.cn/weather_mini?citykey='+self.Weather_ID)
            rep.encoding = 'utf-8'
            str_x = rep.json()
            weatcher_result_txt = json.dumps(str_x, ensure_ascii = False, indent = 6)
            # 将 JSON 对象转换为 Python 字典
            json_data = json.loads(weatcher_result_txt)
            self.textEdit_Weather.setText('')
            # self.textEdit_Weather.setText(weatcher_result_txt)
            txt_city = json_data['data']['city']
            txt_current_temp = json_data['data']['wendu']   #实时温度
            txt_info = json_data['data']['ganmao']          #贴士

            txt_forecast_0_date = json_data['data']['forecast'][0]['date']
            txt_forecast_0_type = json_data['data']['forecast'][0]['type']
            txt_forecast_0_high = json_data['data']['forecast'][0]['high']
            txt_forecast_0_low  = json_data['data']['forecast'][0]['low']

            txt_forecast_1_date = json_data['data']['forecast'][1]['date']
            txt_forecast_1_type = json_data['data']['forecast'][1]['type']
            txt_forecast_1_high = json_data['data']['forecast'][1]['high']
            txt_forecast_1_low  = json_data['data']['forecast'][1]['low']
            
            txt_forecast_2_date = json_data['data']['forecast'][2]['date']
            txt_forecast_2_type = json_data['data']['forecast'][2]['type']
            txt_forecast_2_high = json_data['data']['forecast'][2]['high']
            txt_forecast_2_low  = json_data['data']['forecast'][2]['low']

            txt_forecast_3_date = json_data['data']['forecast'][3]['date']
            txt_forecast_3_type = json_data['data']['forecast'][3]['type']
            txt_forecast_3_high = json_data['data']['forecast'][3]['high']
            txt_forecast_3_low  = json_data['data']['forecast'][3]['low']

            txt_forecast_4_date = json_data['data']['forecast'][4]['date']
            txt_forecast_4_type = json_data['data']['forecast'][4]['type']
            txt_forecast_4_high = json_data['data']['forecast'][4]['high']
            txt_forecast_4_low  = json_data['data']['forecast'][4]['low']

            self.textEdit_Weather.setText(txt_city + '\n' 
                                        + txt_current_temp + '\n'
                                        + txt_info + '\n'
                                        + '-----------------' + '\n'
                                        + txt_forecast_0_date + '\n' 
                                        + txt_forecast_0_type + '\n' 
                                        + txt_forecast_0_high + '\n' 
                                        + txt_forecast_0_low  + '\n'
                                        + '-----------------' + '\n'
                                        + txt_forecast_1_date + '\n' 
                                        + txt_forecast_1_type + '\n' 
                                        + txt_forecast_1_high + '\n' 
                                        + txt_forecast_1_low  + '\n'
                                        + '-----------------' + '\n'
                                        + txt_forecast_2_date + '\n' 
                                        + txt_forecast_2_type + '\n' 
                                        + txt_forecast_2_high + '\n' 
                                        + txt_forecast_2_low  + '\n'
                                        + '-----------------' + '\n'
                                        + txt_forecast_3_date + '\n' 
                                        + txt_forecast_3_type + '\n' 
                                        + txt_forecast_3_high + '\n' 
                                        + txt_forecast_3_low  + '\n'
                                        + '-----------------' + '\n'
                                        + txt_forecast_4_date + '\n' 
                                        + txt_forecast_4_type + '\n' 
                                        + txt_forecast_4_high + '\n' 
                                        + txt_forecast_4_low  + '\n'
                                        + '-----------------' + '\n'
                                        )
            # print (weatcher_result_txt)
        else:
            self.statusBar().showMessage('can not find city id.')

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
            self.pushButton_bing.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')

        elif(self.udp_recv_thread.working_flag == True):

            self.udp_recv_thread.setRun()
            self.udp_connect_flag = False
            self.pushButton_bing.setText('绑定')
            self.pushButton_bing.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')

    # UDP连续发送--------------------------
    def UDP_Send_Continue(self):
        if(self.udp_connect_flag == True):
            # 获得线程运行的状态
            if(self.udp_send_thread.working_flag == False):
                self.udp_send_thread.setRun()
                self.udp_send_thread.start()
                self.pushButton_udpSend_continue.setText('停止')
                self.pushButton_udpSend_continue.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
            elif(self.udp_send_thread.working_flag == True):
                self.udp_send_thread.setRun()
                self.pushButton_udpSend_continue.setText('连续发送')
                self.pushButton_udpSend_continue.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')

    # UDP单次发送--------------------------
    def UDP_Send_Single(self):
        if(self.udp_connect_flag == True):
            if(self.udp_send_thread.working_flag == False):
                self.udp_send_thread.setOneShot()
                self.udp_send_thread.start()

    # UDP接收数据显示----------------------
    def UDP_Recv_ShowInfo(self, str_info, count):
        self.label_udp_recv_count.setText(str(count))




    # # UDP接收函数--------------------------
    # def udp_receiveInfo(self, udpSocket):
    #     udp_recv_count = 0
    #     while True:
    #         try:
    #             # receiveData = udpSocket.recvfrom(1024)
    #             recv_msg, recv_addr = udpSocket.recvfrom(1024)
    #             # print("<<%s:%s"%(str(receiveData[1]),str(receiveData[0])))
    #             # print("<<"+str(recv_addr[0]))
    #             if(str(recv_addr[0]) == "192.168.0.106"):
    #                 # print("yes")
    #                 udp_recv_count = udp_recv_count+1
    #                 # # print("<<"+str(recv_addr[0]))
    #                 print(udp_recv_count)
    #             time.sleep(0.02) 
    #         except Exception as e:
    #             pass
  
# 主函数-------------------------------------
if __name__ == '__main__':

    # global udpSocket
    # global tr
    # global destIp
    # global destPort
    # global udp_recv_count
    # global udp_send_count
    # global udp_connect_flag
    # global udp_send
    # global recv_msg
    # global recv_addr

    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)

    app.setApplicationName("霄哥的神秘工具V1.0")
    app.setStyle("Fusion")

    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet(
        "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
    )

    main_win = mainWin()
    main_win.setWindowTitle('霄哥的神秘工具V1.0')
    #禁止最大化按钮
    main_win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    #禁止拉伸窗口大小
    main_win.setFixedSize(main_win.width(), main_win.height());  
    main_win.show()

    sys.exit(app.exec_())