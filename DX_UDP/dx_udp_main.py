
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 天气API参考：https://zhuanlan.zhihu.com/p/60815507

import sys
import socket
import os
import requests
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp

from Thread_Main import DX_Thread

# ui_main.py中内容
from ui_main import *


# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    # @1-创建udp连接信号
    ConnectSignal = pyqtSignal(bool)
    # @2-创建udp连接标志量
    UDP_Connect_Flag = False
    # @3-天气城市id
    Weather_ID = '101210101'  #默认是杭州


    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        self.statusBar().showMessage('reday.')

        # 安装正则表达式输入验证器
        rx = QtCore.QRegExp("\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b")
        self.lineEdit_Local_IP.setValidator(QRegExpValidator(rx,self))
        # self.lineEdit_Local_IP.setInputMask("000.000.000.000;_")

        # 绑定按钮增加样式
        self.pushButton_bing.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')

        # 按钮绑定触发事件
        self.pushButton_bing.clicked.connect(self.UDP_Connect)
        self.pushButton_udpSend.clicked.connect(self.UDP_Send)

        # 天气查询按键绑定点击触发信号
        self.pushButton_Weather_Check.clicked.connect(self.Weather_Check)
        # 城市查询按键绑定点击触发信号
        self.pushButton_City_Check.clicked.connect(self.City_Check)

        # 绑定网络连接信号
        self.ConnectSignal.connect(self.UDP_Show_Status)

        # 获得本地IP
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        print(self.ip)
        self.lineEdit_Local_IP.setPlaceholderText(self.ip)

        # 创建线程
        self.dx_thread = DX_Thread()
        self.dx_thread.DX_Thread_OutSingal.connect(self.Thread_Info)

        # 线程启动按钮绑定事件
        self.pushButton_thread_start.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
        self.pushButton_thread_start.clicked.connect(self.Thread_Run)

        # 显示界面
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
    def Thread_Info(self, str_info):
        self.textEdit_thread.setText(str_info)


    # --------城市查询------------
    def City_Check(self):
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
                    # print(self.Weather_ID) 
                    break
        file.close()
        # self.textEdit_Weather.setText('----------')


    # --------天气查询------------
    def Weather_Check(self):
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


    # --------显示UDP连接状态------------
    def UDP_Show_Status(self):
        if(self.UDP_Connect_Flag == False):
            self.pushButton_bing.setStyleSheet('QPushButton {background-color: #16A951; color: black;}')
            self.pushButton_bing.setText('绑定')
        elif(self.UDP_Connect_Flag == True):
            self.pushButton_bing.setStyleSheet('QPushButton {background-color: #F20C00; color: black;}')
            self.pushButton_bing.setText('断开')


    # --------UDP连接--------
    def UDP_Connect(self):

        if(self.UDP_Connect_Flag == False):
            self.UDP_Connect_Flag = True
        elif(self.UDP_Connect_Flag == True):
            self.UDP_Connect_Flag = False

        self.ConnectSignal.emit(self.UDP_Connect_Flag)

        # 获得本地IP
        local_ip = self.lineEdit_Local_IP.text()
        
        if(local_ip == ''):
            local_ip = self.ip

        # 获得本地Port
        if(self.lineEdit_Local_Port.text() == ''):
            local_port = 8883
        else:
            local_port = int(self.lineEdit_Local_Port.text())

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((local_ip, local_port))
        except Exception as e:
            print('DX--->Error:', e)
            self.sock.close()
            self.UDP_Connect_Flag = False


    # --------UDP发送--------
    def UDP_Send(self):
        # 获得远端IP
        remote_ip = self.lineEdit_Remote_IP.text()
        
        if(remote_ip == ''):
            remote_ip = "192.168.41.6"

        # 获得远端Port
        if(self.lineEdit_Remote_Port.text() == ''):
            remote_port = 8886
        else:
            remote_port = int(self.lineEdit_Remote_Port.text())

        self.sock.sendto(b'Successful! Message! ',(remote_ip, remote_port))


if __name__ == '__main__':
    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.show()
    sys.exit(app.exec_())