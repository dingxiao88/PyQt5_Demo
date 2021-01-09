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
    if(sender == self.pushButton_DC_FYRun_Up):
        self.udp_send[0] = 54
    elif(sender == self.pushButton_DC_FYRun_Down):
        self.udp_send[0] = 51
    elif(sender == self.pushButton_DC_XHRun_Left):
        self.udp_send[0] = 38
    elif(sender == self.pushButton_DC_XHRun_Right):
        self.udp_send[0] = 53

# FY XH 启停控制复位
def DC_FY_XH_Dir_ControlReset(self):
    sender = self.sender()
    if((sender == self.pushButton_DC_FYRun_Up) or
       (sender == self.pushButton_DC_FYRun_Down) or
       (sender == self.pushButton_DC_XHRun_Left) or
       (sender == self.pushButton_DC_XHRun_Right)):
        self.udp_send[0] = 0
