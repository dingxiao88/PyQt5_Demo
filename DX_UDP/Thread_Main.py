
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time

class DX_Thread(QThread):

    DX_Thread_OutSingal = pyqtSignal(str)

    def __init__(self, parent = None):
        super(DX_Thread, self).__init__(parent)
        self.working_flag = False
        self.Run_Count = 0
        # print('thread init')



    # 线程运行控制
    def setRun(self):
        if(self.working_flag == False):
            self.working_flag = True
            self.DX_Thread_OutSingal.emit('thread set run')

        elif(self.working_flag == True):
            self.working_flag = False
            self.Run_Count = 0
            self.DX_Thread_OutSingal.emit('thread set stop')



    # 线程运行主循环
    def run(self):
        while(self.working_flag == True):
            send_str = 'send count:{0}'.format(self.Run_Count)
            self.Run_Count += 1
            # milliseconds = int(round(time.time() * 1000))
            self.DX_Thread_OutSingal.emit(send_str)
            # self.DX_Thread_OutSingal.emit('count:{0}'.format(self.Run_Count))
            # self.DX_Thread_OutSingal.emit('time:{0}'.format(milliseconds))
            # print('thread send')
            time.sleep(0.01)