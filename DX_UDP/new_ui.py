# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor

from ui_dx_new import *

# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        # 绑定窗口设置函数
        self.btn_close.clicked.connect(self.APP_Close)
        self.btn_maximize_restore.clicked.connect(self.APP_Max)
        self.btn_minimize.clicked.connect(self.APP_Min)

    def APP_Close(self):
        # 关闭程序
        self.close()

    def APP_Max(self):
        # 最大化与复原
        if self.isMaximized():
            self.showNormal()   
        else:
            self.showMaximized()

    def APP_Min(self):
        # 最小化
        self.showMinimized()   

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


if __name__ == '__main__':
    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.setWindowTitle('霄哥的神秘工具V1.0')
    main_win.setWindowFlags(Qt.FramelessWindowHint)     # 无边框
    main_win.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
    main_win.show()
    sys.exit(app.exec_())