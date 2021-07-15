# -*- coding: utf-8 -*-

import sys
import psutil
import socket
import os
import struct
import time

import datetime

# from icecream import ic  #替代print的python库

from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap, QIcon

from ui_dx_new import *

# 从APP文件夹导入
from APP import APP_Fun
from APP import Menu_Fun
from APP import NetWork_Fun
from APP import DX_Control
from APP import Coin_Fun
from Thread_Main import DX_Thread
from dx_SystemTray import dx_SystemTray

from colorpicker import ColorPicker


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
    udp_send_KW_Status = []           #测试KW双网接口
    udp_send_KW_Stoper = []           #测试KW双网接口
    udp_send_KW_ServoConfig = []      #测试KW双网接口
    udp_send_KW_Angel = []            #测试KW双网接口
    DC_FY_CmdRun = False
    DC_XH_CmdRun = False
    # coin自动更新数字货币列表
    coinList = ["bitcoin", "dogecoin", "decentraland", "ethereum"]
    # coin自动更新时间
    autoGetTimeValue = 1
    # coin自动更新标志
    autoGetFlag = False
    # coin自动更新启动标志
    autoGetStart = False
    # coin自动更新tick计数
    autoGetTime_Tick = 0
    # coin自动更新秒计数
    autoGetTime_Second = 0
    # coin自动更新分钟计数
    autoGetTime_Min = 0
    # 程序是否是最小化标志
    appMin_Flag = False
    # 软件底部提示信息str
    current_price2_str = ''
    current_price2 = 0
    current_price2_last = 0

    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        # 显示软件图标  -- 运行python命令的目录必须在文件目录，不然会报错
        self.setWindowIcon(QIcon("./images/me.png"))
        # ic()

        # 配置系统托盘
        self.dx_SystemTray = dx_SystemTray()
        self.dx_SystemTray.dx_SystemTray_Signal.connect(self.SystemTray_Pro)

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
        self.pushButton_coin.clicked.connect(lambda:Menu_Fun.Choose_Menu(self,5))

        # 模式显示DC_Run界面
        self.stackedWidget.setCurrentIndex(0)

        # 创建UDP发送数据
        self.udp_send = []
        for x in range(50):
            self.udp_send.append(0x00)

        #KW双网发送数据初始化
        self.udp_send_KW_Status = []           #测试KW双网接口
        self.udp_send_KW_Stoper = []           #测试KW双网接口
        self.udp_send_KW_ServoConfig = []      #测试KW双网接口
        self.udp_send_KW_Angel = []            #测试KW双网接口
        for x in range(16):
            self.udp_send_KW_Status.append(0x00)
            self.udp_send_KW_Stoper.append(0x00)
            self.udp_send_KW_ServoConfig.append(0x00)
        for x in range(18):
            self.udp_send_KW_Angel.append(0x00)

        #KW状态报文
        self.udp_send_KW_Status[0] = 0x00
        self.udp_send_KW_Status[1] = 0xff
        self.udp_send_KW_Status[2] = 0x00
        self.udp_send_KW_Status[3] = 0x10
        self.udp_send_KW_Status[4] = 0x00
        self.udp_send_KW_Status[5] = 0x00
        self.udp_send_KW_Status[6] = 0x00
        self.udp_send_KW_Status[7] = 0x01
        self.udp_send_KW_Status[8] = 0xff
        self.udp_send_KW_Status[9] = 0xff
        self.udp_send_KW_Status[10] = 0xc8
        self.udp_send_KW_Status[11] = 0xeb
        self.udp_send_KW_Status[12] = 0xff
        self.udp_send_KW_Status[13] = 0x33
        self.udp_send_KW_Status[14] = 0x00
        self.udp_send_KW_Status[15] = 0x00

        #KW制止器控制报文
        self.udp_send_KW_Stoper[0] = 0x00
        self.udp_send_KW_Stoper[1] = 0xff
        self.udp_send_KW_Stoper[2] = 0x00
        self.udp_send_KW_Stoper[3] = 0x10
        self.udp_send_KW_Stoper[4] = 0x00
        self.udp_send_KW_Stoper[5] = 0x00
        self.udp_send_KW_Stoper[6] = 0x00
        self.udp_send_KW_Stoper[7] = 0x01
        self.udp_send_KW_Stoper[8] = 0xff
        self.udp_send_KW_Stoper[9] = 0xff
        self.udp_send_KW_Stoper[10] = 0xc8
        self.udp_send_KW_Stoper[11] = 0xec
        self.udp_send_KW_Stoper[12] = 0xff
        self.udp_send_KW_Stoper[13] = 0x33
        self.udp_send_KW_Stoper[14] = 0x00
        self.udp_send_KW_Stoper[15] = 0x00

        #KW随动配置报文
        self.udp_send_KW_ServoConfig[0] = 0x00
        self.udp_send_KW_ServoConfig[1] = 0xff
        self.udp_send_KW_ServoConfig[2] = 0x00
        self.udp_send_KW_ServoConfig[3] = 0x10
        self.udp_send_KW_ServoConfig[4] = 0x00
        self.udp_send_KW_ServoConfig[5] = 0x00
        self.udp_send_KW_ServoConfig[6] = 0x00
        self.udp_send_KW_ServoConfig[7] = 0x01
        self.udp_send_KW_ServoConfig[8] = 0xff
        self.udp_send_KW_ServoConfig[9] = 0xff
        self.udp_send_KW_ServoConfig[10] = 0xc8
        self.udp_send_KW_ServoConfig[11] = 0xe9
        self.udp_send_KW_ServoConfig[12] = 0xff
        self.udp_send_KW_ServoConfig[13] = 0x33
        self.udp_send_KW_ServoConfig[14] = 0x00
        self.udp_send_KW_ServoConfig[15] = 0x00

        #KW角度命令报文
        self.udp_send_KW_Angel[0] = 0x00
        self.udp_send_KW_Angel[1] = 0xff
        self.udp_send_KW_Angel[2] = 0x00
        self.udp_send_KW_Angel[3] = 0x12
        self.udp_send_KW_Angel[4] = 0x00
        self.udp_send_KW_Angel[5] = 0x00
        self.udp_send_KW_Angel[6] = 0x00
        self.udp_send_KW_Angel[7] = 0x01
        self.udp_send_KW_Angel[8] = 0xff
        self.udp_send_KW_Angel[9] = 0xff
        self.udp_send_KW_Angel[10] = 0xc8
        self.udp_send_KW_Angel[11] = 0xea
        self.udp_send_KW_Angel[12] = 0xff
        self.udp_send_KW_Angel[13] = 0x33
        self.udp_send_KW_Angel[14] = 0x00
        self.udp_send_KW_Angel[15] = 0x00
        self.udp_send_KW_Angel[16] = 0x00
        self.udp_send_KW_Angel[17] = 0x00

        # 测试俯仰和旋回角度
        self.udp_send[5] = 0x01
        self.udp_send[6] = 0x2B
        self.udp_send[7] = 0xE6
        self.udp_send[8] = 0xB6

        # 测试高压控制 | 测试鸣音器控制
        self.udp_send[9] = 0x00

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

        # DC设备鸣音器控制
        self.pushButton_DC_SpeakerCtl.pressed.connect(lambda:DX_Control.DC_Sperker_Control(self))
        # DC设备高压控制
        self.pushButton_DC_MainPower_Ctl.pressed.connect(lambda:DX_Control.DC_MainPower_Control(self))

        # DC设备FY&XH方向操作
        self.pushButton_DC_XHRun_Left.pressed.connect(lambda:DX_Control.DC_FY_XH_Dir_Control(self))
        self.pushButton_DC_XHRun_Right.pressed.connect(lambda:DX_Control.DC_FY_XH_Dir_Control(self))
        # DC设备FY&XH方向操作释放
        self.pushButton_DC_XHRun_Left.released.connect(lambda:DX_Control.DC_FY_XH_Dir_ControlReset(self))
        self.pushButton_DC_XHRun_Right.released.connect(lambda:DX_Control.DC_FY_XH_Dir_ControlReset(self))

        # 数字货币实时价格获取功能
        self.pushButton_getRealPrice.clicked.connect(lambda:Coin_Fun.GetSingleCoinRealPrice(self))
        self.lineEdit_coinPrice.textChanged.connect(lambda:Coin_Fun.GetMoney(self))
        # 自动获取时间选择
        self.pushButton_AutoGet_1M.clicked.connect(lambda:Coin_Fun.SetAutoGetTime(self, 1))
        self.pushButton_AutoGet_5M.clicked.connect(lambda:Coin_Fun.SetAutoGetTime(self, 2))
        self.pushButton_AutoGet_15M.clicked.connect(lambda:Coin_Fun.SetAutoGetTime(self, 3))
        self.pushButton_AutoGet_30M.clicked.connect(lambda:Coin_Fun.SetAutoGetTime(self, 4))
        # 消息自动推送标志
        self.pushButton_AutoGet_Flag.clicked.connect(lambda:Coin_Fun.SetAutoGetTime(self, 5))
        # 自动更新启动
        self.pushButton_startAutoGet.clicked.connect(lambda:Coin_Fun.SetAutoGetTime(self, 6))
        # 自动盈亏
        self.lineEdit_profit_loss.textChanged.connect(lambda:Coin_Fun.GetProfitLoss(self))


        # MQTT图片显示
        pix = QPixmap('1.jpg')
        self.label_mqttPic.setPixmap(pix)

        # websocket图片显示
        pix1 = QPixmap('ESP32_CAM_Real.jpg')
        self.label_mqttPic_2.setPixmap(pix1)
        pix2 = QPixmap('ESP32_CAM_Real1.jpg')
        self.label_mqttPic_3.setPixmap(pix2)

        # 颜色选择按键操作绑定
        self.pushButton_getColor.clicked.connect(self.openColorDialog)

        # 线程启动按钮绑定事件------------
        self.dx_thread = DX_Thread("dx_display", 0.05)
        self.dx_thread.DX_Thread_OutSingal.connect(self.Info_reflash)
        self.dx_thread.setRun()
        self.dx_thread.start()


    # 显示实时价格
    def ShowMoney(self, str_price, mode, index, price):

        # 单价格查询模式
        if(mode == 0):
            self.label_coinRealPrice.setText(str_price)
            self.pushButton_getRealPrice.setEnabled(True)
            self.pushButton_getRealPrice.setText('获取'+ str(mode))

        # 多个价格查询模式
        if(mode == 1):
            if index == 0:
                self.label_showPrice1.setText(str_price)
            elif index == 1:
                self.label_showPrice2.setText(str_price)
                self.current_price2 = price
                self.current_price2_str = str_price
            elif index == 2:
                self.label_showPrice3.setText(str_price)
            elif index == 3:
                self.label_showPrice4.setText(str_price)

            index = index + 1
            if(index < len(self.coinList)):
                Coin_Fun.GetMultiCoinRealPrice(self, index, 0)

            if index == len(self.coinList):
                # self.pushButton_startAutoGet.setEnabled(True)
                self.pushButton_startAutoGet.setText('自动'+ str(mode))
                # 查询程序是否是最小化
                if((self.appMin_Flag == True) or (self.autoGetFlag == True)):
                    if(self.current_price2 > self.current_price2_last):
                        self.dx_SystemTray.showMsg(1, self.current_price2_str)
                    elif(self.current_price2 <= self.current_price2_last):
                        self.dx_SystemTray.showMsg(2, self.current_price2_str)
                    self.current_price2_last = self.current_price2


    def openColorDialog(self):
        # color = QColorDialog.getColor()

        # if color.isValid():
        #     # print(color.name())
        #     print(color.name())
        #     color_R = color.red()
        #     color_G = color.green()
        #     color_B = color.blue()
        #     self.udp_send[40] = color_R
        #     self.udp_send[41] = color_G
        #     self.udp_send[42] = color_B
        #     # print(color_R)

        my_color_picker = ColorPicker(useAlpha=False)
        my_color_picker.DX_Color_OutSingal.connect(self.dx_color)
        picked_color = my_color_picker.hsv2hex(my_color_picker.getColor())
        # print("------->")
        # print(picked_color)


    def dx_color(self,color_r,color_g,color_b):
        print(color_r)
        print(color_g)
        print(color_b)
        self.udp_send[40] = color_r
        self.udp_send[41] = color_g
        self.udp_send[42] = color_b

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

    # 主界面信息显示刷新
    def Info_reflash(self):
        # 显示当前时间
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
        self.label_systemTime.setText(time_str)

        # MQTT显示图片
        pix = QPixmap('1.jpg')
        self.label_mqttPic.setPixmap(pix)
        pix1 = QPixmap('ESP32_CAM_Real.jpg')
        self.label_mqttPic_2.setPixmap(pix1)
        pix2 = QPixmap('ESP32_CAM_Real1.jpg')
        self.label_mqttPic_3.setPixmap(pix2)

        # 数字货币自动更新计数
        self.autoGetTime_Tick = self.autoGetTime_Tick + 1
        if(self.autoGetTime_Tick >= 19):
            self.autoGetTime_Tick = 0
            self.autoGetTime_Second = self.autoGetTime_Second + 1
            if(self.autoGetTime_Second >= 59):
                self.autoGetTime_Second = 0
                self.autoGetTime_Min = self.autoGetTime_Min + 1
                # 自动更细的最大设置时间为30Min
                if(self.autoGetTime_Min >= 30):
                    self.autoGetTime_Min = 0

        # 查询coin自动更新启动标志
        if(self.autoGetStart == True):
            # 自动更新时间到
            if(self.autoGetTime_Min >= self.autoGetTimeValue):
                print('--------------->time up  '+ str(self.autoGetFlag))
                # print()
                self.autoGetTime_Min = 0
                Coin_Fun.GetMultiCoinRealPrice(self, 0, 1)



    # DC信息回显
    def DC_Recv_Info_Display(self, str_info, count, fy_angle, xh_angle):
        # print('--->')
        self.label_dc_Info.setText(str(count)) 
        self.label_fy_angle.setText(str(fy_angle))
        self.label_xh_angle.setText(str(xh_angle))

    
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
    app.setApplicationName("霄哥的神秘工具V1.0")
    main_win = mainWin()
    main_win.setWindowTitle('霄哥的神秘工具V1.0')
    main_win.setWindowFlags(Qt.FramelessWindowHint)     # 无边框
    main_win.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
    main_win.show()
    sys.exit(app.exec_())