# -*- coding: utf-8 -*-


# 按钮设置样式---------------------------
def pushButton_setStyle(which_pushButton,setFlag):
    if(setFlag == 1):
        which_pushButton.setStyleSheet('QPushButton {\
                                        color: rgb(234,237,237);\
                                        background-position: center;\
                                        background-repeat: no-reperat;\
                                        border: none;\
                                        background-color: rgb(85, 170, 255);\
                                        }')
    elif(setFlag == 0):
        which_pushButton.setStyleSheet('QPushButton {\
                                        color: rgb(234,237,237);\
                                        background-position: center;\
                                        background-repeat: no-reperat;\
                                        border: none;\
                                        background-color: rgb(27, 29, 35);\
                                        }\
                                        QPushButton:hover {\
                                        background-color: rgb(33, 37, 43);\
                                        }\
                                        QPushButton:pressed {	\
                                        background-color: rgb(85, 170, 255);\
                                        }')