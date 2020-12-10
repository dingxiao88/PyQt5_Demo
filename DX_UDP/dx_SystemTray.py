

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QAction, QMenu, QWidget)
from PyQt5.QtGui import QRegExpValidator, QIcon, QPixmap, QColor
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp


def setTary(self):
    # 创建托盘对象
    self.tray = QSystemTrayIcon()

    # 创建QIcon对象，用于设置图标（图片过大会出错）
    self.trayIconPix = QPixmap(16,16)
    self.trayIconPix.fill(QColor(100,100,100))
    self.Icon = QIcon(self.trayIconPix)

    # 设置托盘图标（QIcon图标过大或者出错会导致托盘显示不出来）
    self.tray.setIcon(self.Icon)

    # 创建QAction
    showAction = QAction("&显示", self, triggered = self.showApp_dx)
    quitAction = QAction("&退出", self, triggered = self.closeApp_dx)
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


def showMsg(self):
    self.tray.showMessage(
        "霄哥的程序",
        "程序缩小至系统托盘!",
        QSystemTrayIcon.Information,
        2000
    )

