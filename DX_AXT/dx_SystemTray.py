

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QAction, QMenu, QStyle, QWidget)
# from PyQt5.QtWidgets import (

#     QApplication, QMainWindow,

#     QLabel, QGridLayout, QWidget,

#     QCheckBox, QSystemTrayIcon,

#     QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp)
from PyQt5.QtGui import QRegExpValidator, QIcon, QPixmap, QColor
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp


# def setTary(self):
#     # 创建托盘对象
#     self.tray = QSystemTrayIcon()

#     # 创建QIcon对象，用于设置图标（图片过大会出错）
#     # self.trayIconPix = QPixmap(16,16)
#     # self.trayIconPix.fill(QColor(100,100,100))
#     self.trayIconPix = QPixmap("./images/me.png")
#     self.Icon = QIcon(self.trayIconPix)

#     # 设置托盘图标（QIcon图标过大或者出错会导致托盘显示不出来）
#     self.tray.setIcon(self.Icon)

#     # 创建QAction
#     showAction = QAction("&显示", self, triggered = self.showApp_dx)
#     quitAction = QAction("&退出", self, triggered = self.closeApp_dx)
#     # 创建菜单对象
#     self.trayMenu = QMenu(self)
#     # 将动作对象添加到菜单
#     self.trayMenu.addAction(showAction)
#     # 增加分割线
#     self.trayMenu.addSeparator()
#     self.trayMenu.addAction(quitAction)
#     # 将菜单栏加入到右键按钮中
#     self.tray.setContextMenu(self.trayMenu)

#     self.tray.show()


# def showMsg(self, ):
#     self.tray.showMessage(
#         "霄哥的神秘工具",
#         "程序缩小至系统托盘!",
#         QSystemTrayIcon.Information,
#         2000
#     )

# 使用类的方法对系统托盘类进行改造
class dx_SystemTray(QWidget):

    dx_SystemTray_Signal = pyqtSignal(str)

    def __init__(self, parent = None):
        super(dx_SystemTray, self).__init__(parent)

        self.tray = QSystemTrayIcon()

        # # 创建QIcon对象，用于设置图标（图片过大会出错） -- 运行python命令的目录必须在文件目录，不然会报错
        # # self.trayIconPix = QPixmap(16,16)
        # # self.trayIconPix.fill(QColor(100,100,100))
        # self.trayIconPix = QPixmap("./images/me.png")
        # self.Icon = QIcon(self.trayIconPix)

        # # 设置托盘图标（QIcon图标过大或者出错会导致托盘显示不出来）
        # self.tray.setIcon(self.Icon)

        self.tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        # 创建QAction
        showAction = QAction("&显示", self, triggered = self.showApp)
        quitAction = QAction("&退出", self, triggered = self.closeApp)
        # 创建菜单对象
        self.trayMenu = QMenu(self)
        # 将动作对象添加到菜单
        self.trayMenu.addAction(showAction)
        # 增加分割线
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(quitAction)
        # 将菜单栏加入到右键按钮中
        self.tray.setContextMenu(self.trayMenu)

        self.tray.show()

    # 显示程序主页面
    def showApp(self):
        self.dx_SystemTray_Signal.emit("show")

    # 程序退出
    def closeApp(self):
        self.dx_SystemTray_Signal.emit("close")

    # 显示消息
    def showMsg(self, Msg_type, Msg_str):

        if(Msg_type == 1):
            showMsgType = QSystemTrayIcon.Information
        elif(Msg_type == 2):
            showMsgType = QSystemTrayIcon.Warning
        elif(Msg_type == 3):
            showMsgType = QSystemTrayIcon.Critical

        self.tray.showMessage(
            "霄哥的神秘工具",
            # "程序缩小至系统托盘!",
            Msg_str,
            Msg_type,
            2000
        )