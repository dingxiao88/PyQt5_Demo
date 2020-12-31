# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPropertyAnimation
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

        # 绑定设置menu显示
        self.btn_toggle_menu.clicked.connect((lambda: self.Show_Menu(200)))

        # 功能选项切换
        self.pushButton_dc_run.clicked.connect(lambda:self.Choose_Menu(1))
        self.pushButton_weather.clicked.connect(lambda:self.Choose_Menu(2))
        self.pushButton_config.clicked.connect(lambda:self.Choose_Menu(3))
        self.pushButton_setting.clicked.connect(lambda:self.Choose_Menu(4))
        


    def Choose_Menu(self, btn_index):
        self.pushButton_dc_run.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-monitor.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')

        self.pushButton_weather.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-rain.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')

        self.pushButton_config.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-equalizer.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')

        self.pushButton_setting.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-settings.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')




        if(btn_index == 1):
            self.pushButton_dc_run.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-monitor.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                border-right: 5px solid rgb(44, 49, 60);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')
            self.stackedWidget.setCurrentIndex(0)

        elif(btn_index == 2):
            self.pushButton_weather.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-rain.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                border-right: 5px solid rgb(44, 49, 60);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')
            self.stackedWidget.setCurrentIndex(1)

        elif(btn_index == 3):
            self.pushButton_config.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-equalizer.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                border-right: 5px solid rgb(44, 49, 60);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')
            self.stackedWidget.setCurrentIndex(2)

        elif(btn_index == 4):
            self.pushButton_setting.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-settings.png);\
                                                background-position: left center;\
                                                background-repeat: no-repeat;\
                                                border: none;\
                                                border-left: 28px solid rgb(27, 29, 35);\
                                                border-right: 5px solid rgb(44, 49, 60);\
                                                background-color: rgb(27, 29, 35);\
                                                text-align: left;\
                                                padding-left: 45px;}\
                                                QPushButton:hover {\
                                                background-color: rgb(33, 37, 43);\
                                                border-left: 28px solid rgb(33, 37, 43);\
                                                }\
                                                QPushButton:pressed {	\
                                                background-color: rgb(85, 170, 255);\
                                                border-left: 28px solid rgb(85, 170, 255);\
                                                }')




    # 显示菜单过度动画
    def Show_Menu(self, maxWidth):
        # GET WIDTH
        width = self.frame_left_menu.width()
        maxExtend = maxWidth
        standard = 70

        # SET MAX WIDTH
        if width == 70:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


    def APP_Close(self):
        # 关闭程序
        self.close()

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