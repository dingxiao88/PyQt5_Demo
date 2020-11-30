# -*- coding: utf-8 -*-

import sys
import socket

from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtCore import pyqtSignal, Qt

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

        self.pushButton_bing.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')

        self.pushButton_bing.clicked.connect(self.UDP_Connect)
        self.pushButton_udpSend.clicked.connect(self.UDP_Send)

        self.ConnectSignal.connect(self.UDP_Show_Status)

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
            local_ip = "192.168.41.4"

        # 获得本地Port
        if(self.lineEdit_Local_Port.text() == ''):
            local_port = 8883
        else:
            local_port = int(self.lineEdit_Local_Port.text())

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.bind(("192.168.41.4", 8883))
        self.sock.bind((local_ip, local_port))


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