
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

# 运行外部命令
import subprocess

import shutil

# 颜色识取器
from colorpicker import ColorPicker

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


# Meter_Main48.py中内容
from Meter_Main48 import *
# Meter_Main96.py中内容
from Meter_Main96 import *
# Meter_Sel.py中内容
from Meter_Sel import *


# 软件选择界面
class mainWin(QMainWindow, Ui_MainWindow):

    # 自定义信号用于切换到48表主界面
    show_main_win48_signal = pyqtSignal()
    # 自定义信号用于切换到96表主界面
    show_main_win96_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        # 绑定按键响应函数
        # 1 表盘样式选择-48
        self.pushButton_style_choose1.clicked.connect(self.Gague_StyleChoose_48)
        # 2 表盘样式选择-96
        self.pushButton_style_choose2.clicked.connect(self.Gague_StyleChoose_96)

    def Gague_StyleChoose_48(self):
        self.show_main_win48_signal.emit()

    def Gague_StyleChoose_96(self):
        self.show_main_win96_signal.emit()

# 显示96表盘编辑界面
def show_main_96():
    main_win_96.show()
    main_win.hide()

# 显示48表盘编辑界面
def show_main_48():
    main_win_48.show()
    main_win.hide()

# 显示选择表盘
def show_main_sel():
    main_win_48.hide()
    main_win_96.hide()
    main_win.show()


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

    # 软件主界面-48
    main_win_48 = mainWin_48()
    main_win_48.show_sel_win_signal.connect(show_main_sel)
    main_win_48.setWindowTitle('智能48表盘生成器V1.0')
    #禁止最大化按钮
    main_win_48.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    #禁止拉伸窗口大小
    main_win_48.setFixedSize(main_win_48.width(), main_win_48.height());  


    # 软件主界面-96
    main_win_96 = mainWin_96()
    main_win_96.show_sel_win_signal.connect(show_main_sel)
    main_win_96.setWindowTitle('智能96表盘生成器V1.0')
    #禁止最大化按钮
    main_win_96.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    #禁止拉伸窗口大小
    main_win_96.setFixedSize(main_win_96.width(), main_win_96.height());  


    # 软件启动选择界面
    main_win = mainWin()
    main_win.show_main_win48_signal.connect(show_main_48)
    main_win.show_main_win96_signal.connect(show_main_96)
    main_win.setWindowTitle('智能表盘生成器V1.0')
    #禁止最大化按钮
    main_win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    #禁止拉伸窗口大小
    main_win.setFixedSize(main_win.width(), main_win.height()); 


    # 软件启动选择界面
    main_win.show()

    sys.exit(app.exec_())