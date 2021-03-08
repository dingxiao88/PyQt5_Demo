# -*- coding: utf-8 -*-
from APP import Element_Style


# FY运行控制--------------------------
def DC_FYRun(self):
    if(self.DC_FY_CmdRun == False):
        self.DC_FY_CmdRun = True
        self.pushButton_DC_FYRunCtl.setText("停止")
        self.udp_send[3] = 1  #FY运行
        Element_Style.pushButton_setStyle(self.pushButton_DC_FYRunCtl, 1)

    else:
        self.DC_FY_CmdRun = False
        self.pushButton_DC_FYRunCtl.setText("启动")
        self.udp_send[3] = 0  #FY停止
        Element_Style.pushButton_setStyle(self.pushButton_DC_FYRunCtl, 0)

# XH运行控制--------------------------
def DC_XHRun(self):
    if(self.DC_XH_CmdRun == False):
        self.DC_XH_CmdRun = True
        self.pushButton_DC_XHRunCtl.setText("停止")
        self.udp_send[4] = 1  #XH运行
        Element_Style.pushButton_setStyle(self.pushButton_DC_XHRunCtl, 1)

    else:
        self.DC_XH_CmdRun = False
        self.pushButton_DC_XHRunCtl.setText("启动")
        self.udp_send[4] = 0  #XH停止
        Element_Style.pushButton_setStyle(self.pushButton_DC_XHRunCtl, 0)

# FY XH 启停控制
def DC_FY_XH_Dir_Control(self):
    sender = self.sender()
    # if(sender == self.pushButton_DC_FYRun_Up):
    #     self.udp_send[0] = 54
    if(sender == self.pushButton_DC_FYRun_Down):
        self.udp_send[0] = 51
    elif(sender == self.pushButton_DC_XHRun_Left):
        self.udp_send[0] = 38
    elif(sender == self.pushButton_DC_XHRun_Right):
        self.udp_send[0] = 53

# 装置鸣音器控制
def DC_Sperker_Control(self):
    sender = self.sender()
    if(sender == self.pushButton_DC_SpeakerCtl):
        if(self.udp_send[9] == 0x00):
            self.udp_send[9] = 0x02
            self.pushButton_DC_SpeakerCtl.setStyleSheet ('''QPushButton {
                                                                    background-image: url(:/images_icons_20/images/icons/20x20/cil-volume-high.png);
                                                                    background-position: center;
                                                                    background-repeat: no-reperat;
                                                                    border: none;
                                                                    background-color: rgb(27, 29, 35);
                                                                }
                                                                QPushButton:hover {
                                                                    background-color: rgb(33, 37, 43);
                                                                }
                                                                QPushButton:pressed {	
                                                                    background-color: rgb(85, 170, 255);
                                                                }''')

        elif(self.udp_send[9] == 0x02):
            self.udp_send[9] = 0x00
            self.pushButton_DC_SpeakerCtl.setStyleSheet ('''QPushButton {
                                                                background-image: url(:/images_icons_20/images/icons/20x20/cil-volume-off.png);
                                                                background-position: center;
                                                                background-repeat: no-reperat;
                                                                border: none;
                                                                background-color: rgb(27, 29, 35);
                                                                }
                                                                QPushButton:hover {
                                                                    background-color: rgb(33, 37, 43);
                                                                }
                                                                QPushButton:pressed {	
                                                                    background-color: rgb(85, 170, 255);
                                                                }''')


# 装置高压控制
def DC_MainPower_Control(self):
    sender = self.sender()
    if(sender == self.pushButton_DC_MainPower_Ctl):
        if(self.udp_send[9] == 0x00):
            self.udp_send[9] = 0x01
            self.pushButton_DC_MainPower_Ctl.setStyleSheet ('''QPushButton {
                                                                    background-image: url(:/images_icons_20/images/icons/20x20/cil-x.png);
                                                                    background-position: center;
                                                                    background-repeat: no-reperat;
                                                                    border: none;
                                                                    background-color: rgb(27, 29, 35);
                                                                }
                                                                QPushButton:hover {
                                                                    background-color: rgb(33, 37, 43);
                                                                }
                                                                QPushButton:pressed {	
                                                                    background-color: rgb(85, 170, 255);
                                                                }''')

        elif(self.udp_send[9] == 0x01):
            self.udp_send[9] = 0x00
            self.pushButton_DC_MainPower_Ctl.setStyleSheet ('''QPushButton {
                                                                background-image: url(:/images_icons_20/images/icons/20x20/cil-check-alt.png);
                                                                background-position: center;
                                                                background-repeat: no-reperat;
                                                                border: none;
                                                                background-color: rgb(27, 29, 35);
                                                                }
                                                                QPushButton:hover {
                                                                    background-color: rgb(33, 37, 43);
                                                                }
                                                                QPushButton:pressed {	
                                                                    background-color: rgb(85, 170, 255);
                                                                }''')

# FY XH 启停控制复位
def DC_FY_XH_Dir_ControlReset(self):
    sender = self.sender()
    if((sender == self.pushButton_DC_FYRun_Up) or
       (sender == self.pushButton_DC_FYRun_Down) or
       (sender == self.pushButton_DC_XHRun_Left) or
       (sender == self.pushButton_DC_XHRun_Right)):
        self.udp_send[0] = 0
