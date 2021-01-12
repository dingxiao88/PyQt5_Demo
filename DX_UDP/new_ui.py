# -*- coding: utf-8 -*-

import sys
import psutil
import socket
import os
import struct
import time

import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap

from ui_dx_new import *

# 从APP文件夹导入
from APP import APP_Fun
from APP import Menu_Fun
from APP import NetWork_Fun
from APP import DX_Control
from Thread_Main import DX_Thread


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
    DC_FY_CmdRun = False
    DC_XH_CmdRun = False

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

        # 创建UDP发送数据
        self.udp_send = []
        for x in range(50):
            self.udp_send.append(0x00)

        # 初始化本地网卡
        NetWork_Fun.Init_Local_Interface(self)
        self.comboBox_LocalInterface.currentIndexChanged.connect(lambda:NetWork_Fun.On_interface_selection_change(self))
        # UDP连接
        self.pushButton_bing.clicked.connect(lambda:NetWork_Fun.UDP_Connect(self))
        # UDP单击发送
        self.pushButton_udpSend.clicked.connect(lambda:NetWork_Fun.UDP_Send_Single(self))
        # UDP连续发送
        self.pushButton_udpSend_continue.clicked.connect(lambda:NetWork_Fun.UDP_Send_Continue(self))

        # DC设备FY&XH运行操作
        self.pushButton_DC_FYRunCtl.clicked.connect(lambda:DX_Control.DC_FYRun(self))
        self.pushButton_DC_XHRunCtl.clicked.connect(lambda:DX_Control.DC_XHRun(self))

        # DC设备FY&XH方向操作
        self.pushButton_DC_FYRun_Up.pressed.connect(lambda:DX_Control.DC_FY_XH_Dir_Control(self))
        self.pushButton_DC_FYRun_Down.pressed.connect(lambda:DX_Control.DC_FY_XH_Dir_Control(self))
        self.pushButton_DC_XHRun_Left.pressed.connect(lambda:DX_Control.DC_FY_XH_Dir_Control(self))
        self.pushButton_DC_XHRun_Right.pressed.connect(lambda:DX_Control.DC_FY_XH_Dir_Control(self))
        # DC设备FY&XH方向操作释放
        self.pushButton_DC_FYRun_Up.released.connect(lambda:DX_Control.DC_FY_XH_Dir_ControlReset(self))
        self.pushButton_DC_FYRun_Down.released.connect(lambda:DX_Control.DC_FY_XH_Dir_ControlReset(self))
        self.pushButton_DC_XHRun_Left.released.connect(lambda:DX_Control.DC_FY_XH_Dir_ControlReset(self))
        self.pushButton_DC_XHRun_Right.released.connect(lambda:DX_Control.DC_FY_XH_Dir_ControlReset(self))

        # MQTT图片显示
        pix = QPixmap('1.jpg')
        self.label_mqttPic.setPixmap(pix)

        # 线程启动按钮绑定事件------------
        self.dx_thread = DX_Thread("dx_display", 0.05)
        self.dx_thread.DX_Thread_OutSingal.connect(self.Info_reflash)
        self.dx_thread.setRun()
        self.dx_thread.start()


    # 主界面信息显示刷新
    def Info_reflash(self):
        # 显示当前时间
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
        self.label_systemTime.setText(time_str)
        pix = QPixmap('1.jpg')
        self.label_mqttPic.setPixmap(pix)

    # DC信息回显
    def DC_Recv_Info_Display(self, str_info, count):
        # print('--->')
        self.label_dc_Info.setText(str(count))

    
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