# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPropertyAnimation


 # 功能菜单选择
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

    self.pushButton_about.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-settings.png);\
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
        self.pushButton_about.setStyleSheet('QPushButton {background-image: url(:/images_icons_20/images/icons/20x20/cil-settings.png);\
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