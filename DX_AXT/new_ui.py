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

    #------------------------------#AXT模拟FK设备---------------------------------
    udp_send_AXT_FK_askStatus = []    #AXT模拟FK设备-状态询问报文
    udp_send_AXT_FK_ctlAXT = []       #AXT模拟FK设备-装置控制报文
    udp_send_AXT_FK_cmdFS = []        #AXT模拟FK设备-FS命令报文
    udp_send_AXT_FK_persureSet = []   #AXT模拟FK设备-气瓶压力设定报文
    udp_send_AXT_FK_envInfo = []      #AXT模拟FK设备-环境信息报文

    AXT_RecvSend_ID = 0x42
    AXT_PrioID_Top  = 0x00
    AXT_PrioID_High = 0x08
    AXT_PrioID_Low  = 0x10
    #------------------------------#AXT模拟FK设备 End---------------------------------

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

        # 配置系统托盘-20220921-系统托盘功能不正常是因为托盘图片不对(me.png)
        self.dx_SystemTray = dx_SystemTray()
        self.dx_SystemTray.dx_SystemTray_Signal.connect(self.SystemTray_Pro)
        # self.dx_SystemTray.showMsg(1, "程序缩小至系统托盘!")

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
        self.pushButton_axt_run.clicked.connect(lambda:Menu_Fun.Choose_Menu(self,6))

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

        #AXT模拟FK设备CAN发送数据初始化
        self.udp_send_AXT_FK_askStatus = []    #测试AXT-FK设备-工作状态询问报文
        self.udp_send_AXT_FK_ctlAXT = []       #测试AXT-FK设备-装置控制报文
        self.udp_send_AXT_FK_cmdFS = []        #测试AXT-FK设备-FS命令报文
        self.udp_send_AXT_FK_persureSet = []   #测试AXT-FK设备-气瓶压力设定报文
        self.udp_send_AXT_FK_envInfo = []      #测试AXT-FK设备-环境信息报文

        for x in range(16):
            self.udp_send_KW_Status.append(0x00)
            self.udp_send_KW_Stoper.append(0x00)
            self.udp_send_KW_ServoConfig.append(0x00)
        for x in range(18):
            self.udp_send_KW_Angel.append(0x00)

        # AXT数据初始化
        # 母线控制
        self.cmd_mainpower_ctl = 0
        # 控制1~6管前盖状态 0:关闭 1:打开
        self.cmd_front_case1 = 0
        self.cmd_front_case2 = 0
        self.cmd_front_case3 = 0
        self.cmd_front_case4 = 0
        self.cmd_front_case5 = 0
        self.cmd_front_case6 = 0
        # FY控制
        self.cmd_fy_ctl = 0
        # XH控制
        self.cmd_xh_ctl = 0
        # 控制俯仰、旋回角度
        self.cmd_fy_angle = 0.0
        self.cmd_xh_angle = -90.0
        # 气源压力
        self.cmd_persure = 10.0
        # 1~6管气瓶压力
        self.cmd_persure1 = 10.0
        self.cmd_persure2 = 10.0
        self.cmd_persure3 = 10.0
        self.cmd_persure4 = 10.0
        self.cmd_persure5 = 10.0
        self.cmd_persure6 = 10.0
        # 设定环境温度（温度℃）
        self.cmd_temperture = 20.0
        # 设定海况（0~9级）
        self.cmd_seastate = 0
        # 1~6管FS命令
        self.cmd_fs1 = 0
        self.cmd_fs2 = 0
        self.cmd_fs3 = 0
        self.cmd_fs4 = 0
        self.cmd_fs5 = 0
        self.cmd_fs6 = 0

        # 创建AXT数据字典
        self.axt_data_dict = {

            #-各管Bomb在位信息 0：无  1：有
            "AXT_Tube1_BombStatus" : 0,
            "AXT_Tube2_BombStatus" : 0,
            "AXT_Tube3_BombStatus" : 0,
            "AXT_Tube4_BombStatus" : 0,
            "AXT_Tube5_BombStatus" : 0,
            "AXT_Tube6_BombStatus" : 0,

            # - 充气及驱动机柜状态    0：正常  1：故障
            "AXT_DevPart1_Status" : 1,
            # - 发射管及驱动机构状态  0：正常  1：故障
            "AXT_DevPart2_Status" : 1,
            # - 各管电缆回插状态      0：未接通  1：接通
            "AXT_Tube1_CableStatus" : 0,
            "AXT_Tube2_CableStatus" : 0,
            "AXT_Tube3_CableStatus" : 0,
            "AXT_Tube4_CableStatus" : 0,
            "AXT_Tube5_CableStatus" : 0,
            "AXT_Tube6_CableStatus" : 0,

            # - 各管前盖状态  0：正常  1：故障  2：开盖中  3：开盖到位  4：关盖中  5：关盖到位
            "AXT_Tube1_FrontCaseStatus" : 1,
            "AXT_Tube2_FrontCaseStatus" : 1,
            "AXT_Tube3_FrontCaseStatus" : 1,
            "AXT_Tube4_FrontCaseStatus" : 1,
            "AXT_Tube5_FrontCaseStatus" : 1,
            "AXT_Tube6_FrontCaseStatus" : 1,
            # - 各管前盖反馈状态有效标志
            # - FY角度
            # - XH角度

            # -发射命令反馈

             # -关机报文  0：未关机  1：关机
            "AXT_Dev_Close" : 1,

            # -总气压值
            "AXT_Dev_AirPressure" : 0.0,
            # -各管气压值
            "AXT_Tube1_AirPressure" : 0.0,
            "AXT_Tube2_AirPressure" : 0.0,
            "AXT_Tube3_AirPressure" : 0.0,
            "AXT_Tube4_AirPressure" : 0.0,
            "AXT_Tube5_AirPressure" : 0.0,
            "AXT_Tube6_AirPressure" : 0.0,

            # -各管加热状态  0：不加热  1：加热
            "AXT_Tube1_Warm_Status" : 0,
            "AXT_Tube2_Warm_Status" : 0,
            "AXT_Tube3_Warm_Status" : 0,
            "AXT_Tube4_Warm_Status" : 0,
            "AXT_Tube5_Warm_Status" : 0,
            "AXT_Tube6_Warm_Status" : 0,

            # -各管温度
            "AXT_Tube1_Temperature" : 0.0,
            "AXT_Tube2_Temperature" : 0.0,
            "AXT_Tube3_Temperature" : 0.0,
            "AXT_Tube4_Temperature" : 0.0,
            "AXT_Tube5_Temperature" : 0.0,
            "AXT_Tube6_Temperature" : 0.0

        }
        # print(self.axt_data_dict)

        # AXT发送报文ID
        self.AXT_Send_MesgID = 0

        #AXT双网发送数据初始化
        for x in range(13):
            self.udp_send_AXT_FK_askStatus.append(0x00)
            self.udp_send_AXT_FK_ctlAXT.append(0x00)
            self.udp_send_AXT_FK_cmdFS.append(0x00)
            self.udp_send_AXT_FK_persureSet.append(0x00)
            self.udp_send_AXT_FK_envInfo.append(0x00)

        #@1-AXT FK设备状态询问报文------------------------------------------------------
        self.udp_send_AXT_FK_askStatus[0] = 0x88                  #扩展帧-数据帧
        self.udp_send_AXT_FK_askStatus[1] = self.AXT_PrioID_High  #优先级高
        self.udp_send_AXT_FK_askStatus[2] = 0x00                  #备用
        self.udp_send_AXT_FK_askStatus[3] = self.AXT_RecvSend_ID  #接收端ID(高4bit)|发送端ID(低4bit)
        self.udp_send_AXT_FK_askStatus[4] = 0x01                  #报文序号
        #--数据段
        self.udp_send_AXT_FK_askStatus[5] = 0x00  
        self.udp_send_AXT_FK_askStatus[6] = 0x00
        self.udp_send_AXT_FK_askStatus[7] = 0x00
        self.udp_send_AXT_FK_askStatus[8] = 0x00
        self.udp_send_AXT_FK_askStatus[9] = 0x00
        self.udp_send_AXT_FK_askStatus[10] = 0x00
        self.udp_send_AXT_FK_askStatus[11] = 0x00
        self.udp_send_AXT_FK_askStatus[12] = 0x00

        #@2-AXT FK设备装置控制报文------------------------------------------------------
        self.udp_send_AXT_FK_ctlAXT[0] = 0x88                  #扩展帧-数据帧
        self.udp_send_AXT_FK_ctlAXT[1] = self.AXT_PrioID_High  #优先级高
        self.udp_send_AXT_FK_ctlAXT[2] = 0x00                  #备用
        self.udp_send_AXT_FK_ctlAXT[3] = self.AXT_RecvSend_ID  #接收端ID(高4bit)|发送端ID(低4bit)
        self.udp_send_AXT_FK_ctlAXT[4] = 0x02                  #报文序号
        #--数据段
        self.udp_send_AXT_FK_ctlAXT[5] = 0x00  
        self.udp_send_AXT_FK_ctlAXT[6] = 0x00
        self.udp_send_AXT_FK_ctlAXT[7] = 0x00
        self.udp_send_AXT_FK_ctlAXT[8] = 0x00
        self.udp_send_AXT_FK_ctlAXT[9] = 0x00
        self.udp_send_AXT_FK_ctlAXT[10] = 0x00
        self.udp_send_AXT_FK_ctlAXT[11] = 0x00
        self.udp_send_AXT_FK_ctlAXT[12] = 0x00

        #@3-AXT FK设备FS命令报文------------------------------------------------------
        self.udp_send_AXT_FK_cmdFS[0] = 0x88                  #扩展帧-数据帧
        self.udp_send_AXT_FK_cmdFS[1] = self.AXT_PrioID_High  #优先级高
        self.udp_send_AXT_FK_cmdFS[2] = 0x00                  #备用
        self.udp_send_AXT_FK_cmdFS[3] = self.AXT_RecvSend_ID  #接收端ID(高4bit)|发送端ID(低4bit)
        self.udp_send_AXT_FK_cmdFS[4] = 0x03                  #报文序号
        #--数据段
        self.udp_send_AXT_FK_cmdFS[5] = 0x00  
        self.udp_send_AXT_FK_cmdFS[6] = 0x00
        self.udp_send_AXT_FK_cmdFS[7] = 0x00
        self.udp_send_AXT_FK_cmdFS[8] = 0x00
        self.udp_send_AXT_FK_cmdFS[9] = 0x00
        self.udp_send_AXT_FK_cmdFS[10] = 0x00
        self.udp_send_AXT_FK_cmdFS[11] = 0x00
        self.udp_send_AXT_FK_cmdFS[12] = 0x00

        #@4-AXT FK设备气瓶压力设定报文------------------------------------------------------
        self.udp_send_AXT_FK_persureSet[0] = 0x88                  #扩展帧-数据帧
        self.udp_send_AXT_FK_persureSet[1] = self.AXT_PrioID_High  #优先级高
        self.udp_send_AXT_FK_persureSet[2] = 0x00                  #备用
        self.udp_send_AXT_FK_persureSet[3] = self.AXT_RecvSend_ID  #接收端ID(高4bit)|发送端ID(低4bit)
        self.udp_send_AXT_FK_persureSet[4] = 0x04                  #报文序号
        #--数据段
        self.udp_send_AXT_FK_persureSet[5] = 0x00  
        self.udp_send_AXT_FK_persureSet[6] = 0x00
        self.udp_send_AXT_FK_persureSet[7] = 0x00
        self.udp_send_AXT_FK_persureSet[8] = 0x00
        self.udp_send_AXT_FK_persureSet[9] = 0x00
        self.udp_send_AXT_FK_persureSet[10] = 0x00
        self.udp_send_AXT_FK_persureSet[11] = 0x00
        self.udp_send_AXT_FK_persureSet[12] = 0x00

        #@5-AXT FK设备环境信息报文------------------------------------------------------
        self.udp_send_AXT_FK_envInfo[0] = 0x88                  #扩展帧-数据帧
        self.udp_send_AXT_FK_envInfo[1] = self.AXT_PrioID_High  #优先级高
        self.udp_send_AXT_FK_envInfo[2] = 0x00                  #备用
        self.udp_send_AXT_FK_envInfo[3] = self.AXT_RecvSend_ID  #接收端ID(高4bit)|发送端ID(低4bit)
        self.udp_send_AXT_FK_envInfo[4] = 0x05                  #报文序号
        #--数据段
        self.udp_send_AXT_FK_envInfo[5] = 0x00  
        self.udp_send_AXT_FK_envInfo[6] = 0x00
        self.udp_send_AXT_FK_envInfo[7] = 0x00
        self.udp_send_AXT_FK_envInfo[8] = 0x00
        self.udp_send_AXT_FK_envInfo[9] = 0x00
        self.udp_send_AXT_FK_envInfo[10] = 0x00
        self.udp_send_AXT_FK_envInfo[11] = 0x00
        self.udp_send_AXT_FK_envInfo[12] = 0x00


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
        self.udp_send_KW_Stoper[15] = 0x01

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
        # self.udp_send_KW_ServoConfig[15] = 0x00
        # self.udp_send_KW_ServoConfig[15] = 0x01   #XH 启动
        # self.udp_send_KW_ServoConfig[15] = 0x04     #GY 启动
        self.udp_send_KW_ServoConfig[15] = 0x10     #FY 启动
        # self.udp_send_KW_ServoConfig[15] = 0x40     #鸣音器 启动

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
        # self.udp_send_KW_Angel[14] = 0x00  
        # self.udp_send_KW_Angel[15] = 0x00
        # self.udp_send_KW_Angel[16] = 0x00
        # self.udp_send_KW_Angel[17] = 0x00
        self.udp_send_KW_Angel[14] = 0xFF  #FY-FFF7-->-0.1   XH-E001-->-89.99
        self.udp_send_KW_Angel[15] = 0xF7
        self.udp_send_KW_Angel[16] = 0xE0
        self.udp_send_KW_Angel[17] = 0x01

        # 测试俯仰和旋回角度
        self.udp_send[5] = 0x01
        self.udp_send[6] = 0x2B
        self.udp_send[7] = 0xE6
        self.udp_send[8] = 0xB6

        # 测试高压控制 | 测试鸣音器控制
        self.udp_send[9] = 0x00

        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.count5 = 0
        self.count6 = 0
        self.count7 = 0

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


        #-------------------------------------------AXT------------------------------------------
        # AXT-高压开关
        self.pushButton_cmd_mainpower.clicked.connect(lambda:NetWork_Fun.AXT_MainPower_Control(self))
        # AXT-FY开关
        self.pushButton_cmd_fy.clicked.connect(lambda:NetWork_Fun.AXT_FY_Control(self))
        # AXT-XH开关
        self.pushButton_cmd_xh.clicked.connect(lambda:NetWork_Fun.AXT_XH_Control(self))

        # AXT-旋回角度发送按钮
        self.pushButton_cmd_xh_angle.clicked.connect(lambda:NetWork_Fun.AXT_FYXH_Angle_Control(self))
        # AXT-俯仰角度发送按钮
        self.pushButton_cmd_fy_angle.clicked.connect(lambda:NetWork_Fun.AXT_FYXH_Angle_Control(self))
        # AXT-1至6号前盖开闭控制
        self.pushButton_cmd_frontcase1.clicked.connect(lambda:NetWork_Fun.AXT_FrontCast_Control(self, 1))
        self.pushButton_cmd_frontcase2.clicked.connect(lambda:NetWork_Fun.AXT_FrontCast_Control(self, 2))
        self.pushButton_cmd_frontcase3.clicked.connect(lambda:NetWork_Fun.AXT_FrontCast_Control(self, 3))
        self.pushButton_cmd_frontcase4.clicked.connect(lambda:NetWork_Fun.AXT_FrontCast_Control(self, 4))
        self.pushButton_cmd_frontcase5.clicked.connect(lambda:NetWork_Fun.AXT_FrontCast_Control(self, 5))
        self.pushButton_cmd_frontcase6.clicked.connect(lambda:NetWork_Fun.AXT_FrontCast_Control(self, 6))

        # AXT-气源压力设定
        self.pushButton_cmd_persureSet.clicked.connect(lambda:NetWork_Fun.AXT_Persure_Set(self))

        # AXT-气瓶压力设定
        self.pushButton_cmd_persureSet1.clicked.connect(lambda:NetWork_Fun.AXT_Persure_Set(self))
        self.pushButton_cmd_persureSet2.clicked.connect(lambda:NetWork_Fun.AXT_Persure_Set(self))
        self.pushButton_cmd_persureSet3.clicked.connect(lambda:NetWork_Fun.AXT_Persure_Set(self))
        self.pushButton_cmd_persureSet4.clicked.connect(lambda:NetWork_Fun.AXT_Persure_Set(self))
        self.pushButton_cmd_persureSet5.clicked.connect(lambda:NetWork_Fun.AXT_Persure_Set(self))
        self.pushButton_cmd_persureSet6.clicked.connect(lambda:NetWork_Fun.AXT_Persure_Set(self))

        # AXT-环境信息设定-环境温度及海况
        self.pushButton_cmd_environment.clicked.connect(lambda:NetWork_Fun.AXT_EnvironmentInfo_Set(self))
        # self.pushButton_cmd_seaState.clicked.connect(lambda:NetWork_Fun.AXT_EnvironmentInfo_Set(self))

        # AXT-FS命令选择及发送
        self.pushButton_cmd_FS1.clicked.connect(lambda:NetWork_Fun.AXT_FS_Control(self))
        self.pushButton_cmd_FS2.clicked.connect(lambda:NetWork_Fun.AXT_FS_Control(self))
        self.pushButton_cmd_FS3.clicked.connect(lambda:NetWork_Fun.AXT_FS_Control(self))
        self.pushButton_cmd_FS4.clicked.connect(lambda:NetWork_Fun.AXT_FS_Control(self))
        self.pushButton_cmd_FS5.clicked.connect(lambda:NetWork_Fun.AXT_FS_Control(self))
        self.pushButton_cmd_FS6.clicked.connect(lambda:NetWork_Fun.AXT_FS_Control(self))

        # AXT-测试报文选择及发送
        self.pushButton_udpAxtSend.clicked.connect(lambda:NetWork_Fun.AXT_TestMsg_Send(self))
        

        # # AXT-模拟FK-发送状态询问报文
        # self.pushButton_udpAxtSend_askStatus.clicked.connect(lambda:NetWork_Fun.UDP_AXT_Send(self, 1))
        # # AXT-模拟FK-发送装置控制报文
        # self.pushButton_udpAxtSend_ctlDev.clicked.connect(lambda:NetWork_Fun.UDP_AXT_Send(self, 2))

        #--------------------------------AXT END------------------------------------------

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



    # AXT信息回显
    def AXT_Recv_Info_Display(self, str_info, count, fy_angle, xh_angle, str_axt_str, axt_dict, mid):
        # print('--->')
        self.label_dc_Info.setText(str(count)) 
        # AXT调试信息输出
        self.label_AXT_DebguInfo.setText(str_axt_str)

        # if(mid == 2):
        #     print(axt_dict)

        #AXT数据显示
        # print(axt_dict)
        if(axt_dict):

            # 工作状态
            if(mid == 1):
                # -1号有/无DAN
                if(axt_dict["AXT_Tube1_BombStatus"] == 0):
                    self.label_9.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_9.setText("无弹")
                elif(axt_dict["AXT_Tube1_BombStatus"] == 1):
                    self.label_9.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_9.setText("有弹")
                # -2号有/无DAN
                if(axt_dict["AXT_Tube2_BombStatus"] == 0):
                    self.label_29.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_29.setText("无弹")
                elif(axt_dict["AXT_Tube2_BombStatus"] == 1):
                    self.label_29.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_29.setText("有弹")
                # -3号有/无DAN
                if(axt_dict["AXT_Tube3_BombStatus"] == 0):
                    self.label_32.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_32.setText("无弹")
                elif(axt_dict["AXT_Tube3_BombStatus"] == 1):
                    self.label_32.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_32.setText("有弹")
                # -4号有/无DAN
                if(axt_dict["AXT_Tube4_BombStatus"] == 0):
                    self.label_37.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_37.setText("无弹")
                elif(axt_dict["AXT_Tube4_BombStatus"] == 1):
                    self.label_37.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_37.setText("有弹")
                # -5号有/无DAN
                if(axt_dict["AXT_Tube5_BombStatus"] == 0):
                    self.label_38.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_38.setText("无弹")
                elif(axt_dict["AXT_Tube5_BombStatus"] == 1):
                    self.label_38.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_38.setText("有弹")
                # -6号有/无DAN
                if(axt_dict["AXT_Tube6_BombStatus"] == 0):
                    self.label_41.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_41.setText("无弹")
                elif(axt_dict["AXT_Tube6_BombStatus"] == 1):
                    self.label_41.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_41.setText("有弹")

                # -AXT设备工作状态-AXT设备故障信息
                if(axt_dict["AXT_Dev_Status"] == 0):
                    self.label_72.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_72.setText("设备状态:正常")
                    self.label_77.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_77.setText("故障信息:无")
                elif(axt_dict["AXT_Dev_Status"] == 1):
                    self.label_72.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_72.setText("设备状态:故障")
                    self.label_77.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    err_id_str = '{0}'.format(axt_dict["AXT_Dev_ErrorID"])
                    self.label_77.setText("故障信息:" + err_id_str)
                
                # # -AXT设备母线工作状态
                # if(axt_dict["AXT_Dev_MainPower_Status"] == 0):
                #     self.label_80.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                #     self.label_80.setText("母线关闭")
                # elif(axt_dict["AXT_Dev_MainPower_Status"] == 1):
                #     self.label_80.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                #     self.label_80.setText("母线开启")

                # # -AXT设备FY工作状态
                # if(axt_dict["AXT_Dev_FY_Status"] == 0):
                #     self.label_78.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                #     self.label_78.setText("关闭")
                # elif(axt_dict["AXT_Dev_FY_Status"] == 1):
                #     self.label_78.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                #     self.label_78.setText("启动")

                # # -AXT设备XH工作状态
                # if(axt_dict["AXT_Dev_XH_Status"] == 0):
                #     self.label_79.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                #     self.label_79.setText("关闭")
                # elif(axt_dict["AXT_Dev_XH_Status"] == 1):
                #     self.label_79.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                #     self.label_79.setText("启动")

                # -1号回插信号
                if(axt_dict["AXT_Tube1_CableStatus"] == 0):
                    self.label_61.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_61.setText("未连接")
                elif(axt_dict["AXT_Tube1_CableStatus"] == 1):
                    self.label_61.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_61.setText("连接")

                # -2号回插信号
                if(axt_dict["AXT_Tube2_CableStatus"] == 0):
                    self.label_60.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_60.setText("未连接")
                elif(axt_dict["AXT_Tube2_CableStatus"] == 1):
                    self.label_60.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_60.setText("连接")

                # -3号回插信号
                if(axt_dict["AXT_Tube3_CableStatus"] == 0):
                    self.label_62.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_62.setText("未连接")
                elif(axt_dict["AXT_Tube3_CableStatus"] == 1):
                    self.label_62.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_62.setText("连接")

                # -4号回插信号
                if(axt_dict["AXT_Tube4_CableStatus"] == 0):
                    self.label_63.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_63.setText("未连接")
                elif(axt_dict["AXT_Tube4_CableStatus"] == 1):
                    self.label_63.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_63.setText("连接")

                # -5号回插信号
                if(axt_dict["AXT_Tube5_CableStatus"] == 0):
                    self.label_64.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_64.setText("未连接")
                elif(axt_dict["AXT_Tube5_CableStatus"] == 1):
                    self.label_64.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_64.setText("连接")
                    
                # -6号回插信号
                if(axt_dict["AXT_Tube6_CableStatus"] == 0):
                    self.label_65.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_65.setText("未连接")
                elif(axt_dict["AXT_Tube6_CableStatus"] == 1):
                    self.label_65.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_65.setText("连接")

                # print(axt_dict["AXT_Tube6_BombStatus"])

            # 发射命令反馈
            elif(mid == 3):
                # -1号发射命反馈
                tube1_info_str = 'AXT_Tube2_FireInfo:{0}'.format(axt_dict["AXT_Tube2_FireInfo"])
                print(tube1_info_str)
                
                if(axt_dict["AXT_Tube1_FireInfo"] == 0):
                    self.label_55.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_55.setText("关闭")
                elif(axt_dict["AXT_Tube1_FireInfo"] == 1):
                    self.label_55.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_55.setText("打开")
                elif(axt_dict["AXT_Tube1_FireInfo"] == 3):
                    self.label_55.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_55.setText("发射")
                
                # -2号发射命反馈
                if(axt_dict["AXT_Tube2_FireInfo"] == 0):
                    self.label_54.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_54.setText("关闭")
                elif(axt_dict["AXT_Tube2_FireInfo"] == 1):
                    self.label_54.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_54.setText("打开")
                elif(axt_dict["AXT_Tube2_FireInfo"] == 3):
                    self.label_54.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_54.setText("发射")

                # -3号发射命反馈
                if(axt_dict["AXT_Tube3_FireInfo"] == 0):
                    self.label_56.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_56.setText("关闭")
                elif(axt_dict["AXT_Tube3_FireInfo"] == 1):
                    self.label_56.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_56.setText("打开")
                elif(axt_dict["AXT_Tube3_FireInfo"] == 3):
                    self.label_56.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_56.setText("发射")

                # -4号发射命反馈
                if(axt_dict["AXT_Tube4_FireInfo"] == 0):
                    self.label_57.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_57.setText("关闭")
                elif(axt_dict["AXT_Tube4_FireInfo"] == 1):
                    self.label_57.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_57.setText("打开")
                elif(axt_dict["AXT_Tube4_FireInfo"] == 3):
                    self.label_57.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_57.setText("发射")

                # -5号发射命反馈
                if(axt_dict["AXT_Tube5_FireInfo"] == 0):
                    self.label_59.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_59.setText("关闭")
                elif(axt_dict["AXT_Tube5_FireInfo"] == 1):
                    self.label_59.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_59.setText("打开")
                elif(axt_dict["AXT_Tube5_FireInfo"] == 3):
                    self.label_59.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_59.setText("发射")

                # -6号发射命反馈
                # print(axt_dict["AXT_Tube6_FireInfo"])
                if(axt_dict["AXT_Tube6_FireInfo"] == 0):
                    self.label_58.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_58.setText("关闭")
                elif(axt_dict["AXT_Tube6_FireInfo"] == 1):
                    self.label_58.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_58.setText("打开")
                elif(axt_dict["AXT_Tube6_FireInfo"] == 3):
                    self.label_58.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_58.setText("发射")

            # 1-6管前盖状态-XH角度-FY角度
            elif(mid == 2):
                # print(axt_dict["AXT_Tube1_FrontCaseStatus"])
                # -1号前盖状态
                if(axt_dict["AXT_Tube1_FrontCaseStatus"] == 2):
                    self.label_48.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_48.setText("开盖中")
                elif(axt_dict["AXT_Tube1_FrontCaseStatus"] == 3):
                    self.label_48.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_48.setText("开盖到位")
                elif(axt_dict["AXT_Tube1_FrontCaseStatus"] == 4):
                    self.label_48.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_48.setText("关盖中")
                elif(axt_dict["AXT_Tube1_FrontCaseStatus"] == 5):
                    self.label_48.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_48.setText("关盖到位")
                # -2号前盖状态
                if(axt_dict["AXT_Tube2_FrontCaseStatus"] == 2):
                    self.label_49.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_49.setText("开盖中")
                elif(axt_dict["AXT_Tube2_FrontCaseStatus"] == 3):
                    self.label_49.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_49.setText("开盖到位")
                elif(axt_dict["AXT_Tube2_FrontCaseStatus"] == 4):
                    self.label_49.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_49.setText("关盖中")
                elif(axt_dict["AXT_Tube2_FrontCaseStatus"] == 5):
                    self.label_49.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_49.setText("关盖到位")
                # -3号前盖状态
                if(axt_dict["AXT_Tube3_FrontCaseStatus"] == 2):
                    self.label_50.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_50.setText("开盖中")
                elif(axt_dict["AXT_Tube3_FrontCaseStatus"] == 3):
                    self.label_50.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_50.setText("开盖到位")
                elif(axt_dict["AXT_Tube3_FrontCaseStatus"] == 4):
                    self.label_50.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_50.setText("关盖中")
                elif(axt_dict["AXT_Tube3_FrontCaseStatus"] == 5):
                    self.label_50.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_50.setText("关盖到位")
                # -4号前盖状态
                if(axt_dict["AXT_Tube4_FrontCaseStatus"] == 2):
                    self.label_51.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_51.setText("开盖中")
                elif(axt_dict["AXT_Tube4_FrontCaseStatus"] == 3):
                    self.label_51.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_51.setText("开盖到位")
                elif(axt_dict["AXT_Tube4_FrontCaseStatus"] == 4):
                    self.label_51.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_51.setText("关盖中")
                elif(axt_dict["AXT_Tube4_FrontCaseStatus"] == 5):
                    self.label_51.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_51.setText("关盖到位")
                # -5号前盖状态
                if(axt_dict["AXT_Tube5_FrontCaseStatus"] == 2):
                    self.label_52.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_52.setText("开盖中")
                elif(axt_dict["AXT_Tube5_FrontCaseStatus"] == 3):
                    self.label_52.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_52.setText("开盖到位")
                elif(axt_dict["AXT_Tube5_FrontCaseStatus"] == 4):
                    self.label_52.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_52.setText("关盖中")
                elif(axt_dict["AXT_Tube5_FrontCaseStatus"] == 5):
                    self.label_52.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_52.setText("关盖到位")
                # -6号前盖状态
                if(axt_dict["AXT_Tube6_FrontCaseStatus"] == 2):
                    self.label_53.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_53.setText("开盖中")
                elif(axt_dict["AXT_Tube6_FrontCaseStatus"] == 3):
                    self.label_53.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_53.setText("开盖到位")
                elif(axt_dict["AXT_Tube6_FrontCaseStatus"] == 4):
                    self.label_53.setStyleSheet("color:yellow;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_53.setText("关盖中")
                elif(axt_dict["AXT_Tube6_FrontCaseStatus"] == 5):
                    self.label_53.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_53.setText("关盖到位")

                # -旋回INFO
                if(axt_dict["AXT_XH_Info"] == 0):
                    self.label_79.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_79.setText("收到命令")
                elif(axt_dict["AXT_XH_Info"] == 1):
                    self.label_79.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_79.setText("运行中")
                elif(axt_dict["AXT_XH_Info"] == 2):
                    self.label_79.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_79.setText("运行到位")
                elif(axt_dict["AXT_XH_Info"] == 3):
                    self.label_79.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_79.setText("故障")

                # -俯仰INFO
                if(axt_dict["AXT_FY_Info"] == 0):
                    self.label_78.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_78.setText("收到命令")
                elif(axt_dict["AXT_FY_Info"] == 1):
                    self.label_78.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_78.setText("运行中")
                elif(axt_dict["AXT_FY_Info"] == 2):
                    self.label_78.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_78.setText("运行到位")
                elif(axt_dict["AXT_FY_Info"] == 3):
                    self.label_78.setStyleSheet("color:rgb(0, 255, 127);" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_78.setText("故障")


                # -旋回角度
                temp_str = '{0}'.format(round(axt_dict["AXT_XH_RealAngle"], 1))
                self.label_74.setText(temp_str)
                # -俯仰角度
                temp_str = '{0}'.format(round(axt_dict["AXT_FY_RealAngle"], 1))
                self.label_75.setText(temp_str)

            # 1-6管气压
            elif(mid == 5):
                # -1号管气压
                temp_str = '{0}MPa'.format(round(axt_dict["AXT_Tube1_AirPressure"], 1))
                self.label_10.setText(temp_str)
                # -2号管气压
                temp_str = '{0}MPa'.format(round(axt_dict["AXT_Tube2_AirPressure"], 1))
                self.label_28.setText(temp_str)
                # -3号管气压
                temp_str = '{0}MPa'.format(round(axt_dict["AXT_Tube3_AirPressure"], 1))
                self.label_31.setText(temp_str)
                # -4号管气压
                temp_str = '{0}MPa'.format(round(axt_dict["AXT_Tube4_AirPressure"], 1))
                self.label_34.setText(temp_str)
                # -5号管气压
                temp_str = '{0}MPa'.format(round(axt_dict["AXT_Tube5_AirPressure"], 1))
                self.label_36.setText(temp_str)
                # -6号管气压
                temp_str = '{0}MPa'.format(round(axt_dict["AXT_Tube6_AirPressure"], 1))
                self.label_39.setText(temp_str)

            # 1-3管温度
            elif(mid == 6):
                # -1号管加热状态
                if(axt_dict["AXT_Tube1_Heat_Flag"] == 0):
                    # -1号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube1_Temperature"], 1))
                    self.label_43.setStyleSheet("color:white;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_43.setText(temp_str)
                elif(axt_dict["AXT_Tube1_Heat_Flag"] == 1):
                    # -1号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube1_Temperature"], 1))
                    self.label_43.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_43.setText(temp_str)  

                # -2号管加热状态
                if(axt_dict["AXT_Tube2_Heat_Flag"] == 0):
                    # -2号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube2_Temperature"], 1))
                    self.label_45.setStyleSheet("color:white;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_45.setText(temp_str)
                elif(axt_dict["AXT_Tube2_Heat_Flag"] == 1):
                    # -2号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube2_Temperature"], 1))
                    self.label_45.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_45.setText(temp_str)

                # -3号管加热状态
                if(axt_dict["AXT_Tube3_Heat_Flag"] == 0):
                    # -3号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube3_Temperature"], 1))
                    self.label_46.setStyleSheet("color:white;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_46.setText(temp_str)
                elif(axt_dict["AXT_Tube3_Heat_Flag"] == 1):
                    # -3号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube3_Temperature"], 1))
                    self.label_46.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_46.setText(temp_str)

            # 4-6管温度
            elif(mid == 7):
                # -4号管加热状态
                if(axt_dict["AXT_Tube4_Heat_Flag"] == 0):
                    # -4号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube4_Temperature"], 1))
                    self.label_47.setStyleSheet("color:white;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_47.setText(temp_str)
                elif(axt_dict["AXT_Tube4_Heat_Flag"] == 1):
                    # -4号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube4_Temperature"], 1))
                    self.label_47.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_47.setText(temp_str)

                # -5号管加热状态
                if(axt_dict["AXT_Tube5_Heat_Flag"] == 0):
                    # -5号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube5_Temperature"], 1))
                    self.label_44.setStyleSheet("color:white;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_44.setText(temp_str)
                elif(axt_dict["AXT_Tube5_Heat_Flag"] == 1):
                    # -5号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube5_Temperature"], 1))
                    self.label_44.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_44.setText(temp_str)

                # -6号管加热状态
                if(axt_dict["AXT_Tube6_Heat_Flag"] == 0):    
                    # -6号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube6_Temperature"], 1))
                    self.label_42.setStyleSheet("color:white;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_42.setText(temp_str)
                elif(axt_dict["AXT_Tube6_Heat_Flag"] == 1):    
                    # -6号管温度
                    temp_str = '{0}℃'.format(round(axt_dict["AXT_Tube6_Temperature"], 1))
                    self.label_42.setStyleSheet("color:red;" "margin:1px;" "background-color: rgb(33, 37, 43)")
                    self.label_42.setText(temp_str)

            
        # self.label_fy_angle.setText(str(fy_angle))
        # self.label_xh_angle.setText(str(xh_angle))

    
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