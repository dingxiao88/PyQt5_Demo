# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

# 关闭应用
def APP_Close(self):
    # 关闭程序
    # self.close()
    # event.ignore()
    # 程序最小化标志
    self.appMin_Flag = True

    self.hide()
    self.dx_SystemTray.showMsg(1, "程序缩小至系统托盘!")

# 应用窗口最大化
def APP_Max(self):
    icon1 = QtGui.QIcon()
    # 最大化与复原
    if self.isMaximized():
        self.showNormal()  
        icon1.addPixmap(QtGui.QPixmap(":/images_icons_20/images/icons/20x20/cil-window-maximize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_maximize_restore.setIcon(icon1) 
    else:
        self.showMaximized()
        icon1.addPixmap(QtGui.QPixmap(":/images_icons_20/images/icons/20x20/cil-window-restore.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_maximize_restore.setIcon(icon1)

    # 程序最小化标志
    self.appMin_Flag = False

# 应用窗口最小化
def APP_Min(self):
    # 程序最小化标志
    self.appMin_Flag = True
    # 最小化   
    self.showMinimized()   