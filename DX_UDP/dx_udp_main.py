
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket

from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp

# ui_main.py中内容
from ui_main import *


# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    # @1-创建udp连接信号
    ConnectSignal = pyqtSignal(bool)
    # @2-创建udp连接标志量
    UDP_Connect_Flag = False

    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        # 安装正则表达式输入验证器
        rx = QtCore.QRegExp("\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b")
        self.lineEdit_Local_IP.setValidator(QRegExpValidator(rx,self))
        # self.lineEdit_Local_IP.setInputMask("000.000.000.000;_")

        # 绑定按钮增加样式
        self.pushButton_bing.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')

        # 按钮绑定触发事件
        self.pushButton_bing.clicked.connect(self.UDP_Connect)
        self.pushButton_udpSend.clicked.connect(self.UDP_Send)

        # 绑定网络连接信号
        self.ConnectSignal.connect(self.UDP_Show_Status)

        # 获得本地IP
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        print(self.ip)
        self.lineEdit_Local_IP.setPlaceholderText(self.ip)

        self.show()

    def UDP_Show_Status(self):
        if(self.UDP_Connect_Flag == False):
            self.pushButton_bing.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')
            self.pushButton_bing.setText('绑定')
        elif(self.UDP_Connect_Flag == True):
            self.pushButton_bing.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
            self.pushButton_bing.setText('断开')
        
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