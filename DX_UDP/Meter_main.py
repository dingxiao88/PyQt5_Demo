
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
import os
import requests
import json
import threading
import struct
import time
import psutil
from pathlib import Path
from pyqt_led import Led          # https://github.com/Neur1n/pyqt_led


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtSvg


# # 引入设计样式
# # https://github.com/ColinDuquesnoy/QDarkStyleSheet
# import qdarkstyle
# # https://github.com/gmarull/qtmodern
# import qtmodern.styles
# import qtmodern.windows


# Meter.py中内容
from Meter import *


# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        # --------------------------------------------------------------
        # 关闭所有窗口,也不关闭应用程序
        # QApplication.setQuitOnLastWindowClosed(False)
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

       
        # self.renderer =  QtSvg.QSvgRenderer("./meter_images/svg/pointer_2.svg")
        # self.label_pointer.resize(self.renderer.defaultSize())
        # self.painter = QtGui.QPainter(self.label_pointer)
        # self.painter.restore()
        # self.renderer.render(self.painter)
        # self.label_pointer.show()

        defaultPix1 = QtGui.QPixmap("./meter_images/白-纯黑-0-0-0.png")
        self.label_gague.setPixmap(defaultPix1)

        defaultPix2 = QtGui.QPixmap("./meter_images/pointer_2.svg")
        self.label_pointer.setPixmap(defaultPix2)

        
        # 显示界面
        self.show()

    
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

# 主函数-------------------------------------
if __name__ == '__main__':

    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)

    app.setApplicationName("智能表盘生成器V1.0")

    # 设置成Fusion样式
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

    # setup stylesheet
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # qtmodern.styles.dark(app)

    main_win = mainWin()
    main_win.setWindowTitle('智能表盘生成器V1.0')
    #禁止最大化按钮
    main_win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    #禁止拉伸窗口大小
    main_win.setFixedSize(main_win.width(), main_win.height());  
    main_win.show()

    sys.exit(app.exec_())