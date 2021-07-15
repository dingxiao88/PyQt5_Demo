
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import struct

class Thread_Udp_Recv(QThread):

    DX_Thread_OutSingal = pyqtSignal(str, int, float, float)

    def __init__(self, socket, parent = None):
        super(Thread_Udp_Recv, self).__init__(parent)
        self.working_flag = False
        self.Run_Count = 0
        self.socket = socket
        # print('thread init')


    # 线程运行控制
    def setRun(self):
        if(self.working_flag == False):
            self.working_flag = True
            self.DX_Thread_OutSingal.emit('thread set run', 1, 0, 0)

        elif(self.working_flag == True):
            self.working_flag = False
            self.Run_Count = 0
            self.DX_Thread_OutSingal.emit('thread set stop', 0, 0, 0)


    # 线程运行主循环
    def run(self):
        while(self.working_flag == True):
            try:
                # receiveData = udpSocket.recvfrom(1024)
                recv_msg, recv_addr = self.socket.recvfrom(1024)
                # print("<<%s:%s"%(str(receiveData[1]),str(receiveData[0]))) 
                # print("<<"+str(recv_addr[1]))
                if((str(recv_addr[0]) == "168.6.4.9") and (str(recv_addr[1]) == "21785")):
                # if((str(recv_addr[0]) == "192.168.0.106") or (str(recv_addr[0]) == "192.168.31.79") or (str(recv_addr[0]) == "10.0.0.24")):

                    # msg1 = struct.unpack('!18B',recv_msg)  #!网络字节顺序 20字节 B unsigned char
                    # print(msg1[15])

                    # 接收到的数据长度
                    # print(str(len(recv_msg)))

                    # msg = recv_msg.decode('utf-8')
                    # # msg = '来自IP:{}端口:{}:\n{}\n'.format(recv_addr[0], recv_addr[1], msg)
                    # msg = '来自IP:{}端口:{}:\n'.format(recv_addr[0], recv_addr[1])
                    # print(msg)

                    data_len = len(recv_msg)

                    # 数据报文18B-随动角度报文
                    if(data_len == 18):
                        data_18 = struct.unpack('!18B',recv_msg)
                        # //@-MK3设备-FY输入角度
                        # temp1 = (int)(Computer_NetRecv_Data[13]&0xff);
                        # temp2 = (int)(Computer_NetRecv_Data[12]&0xff);
                        # temp3 = (int)((temp1*256)+temp2);
                        # if(temp1>=128)
                        # {
                        # temp3 = (temp3 - 65535) - 1;
                        # }
                        # MK3_FY_InputAngle = (float)((temp3*180)/16384.0);

                        # 俯仰角度 [fff7] -> -0.09
                        temp_fy_angle = (data_18[14] * 256) + data_18[15]
                        if(data_18[14] > 128):
                            temp_fy_angle = temp_fy_angle - 65536
                        fy_angle = ((temp_fy_angle*180)/16384.0)
                        fy_angle = round(fy_angle, 2)
                        # print(fy_angle)
                        # 0.19775390625

                        # 旋回角度 [e001] -> -89.98
                        temp_xh_angle = (data_18[16] * 256) + data_18[17]
                        if(data_18[16] > 128):
                            temp_xh_angle = temp_xh_angle - 65536
                        xh_angle = ((temp_xh_angle*180)/16384.0)
                        xh_angle = round(xh_angle, 2)
                        # print(xh_angle) 
                        # -91.95556640625

                    # 数据报文20B-随动状态报文
                    elif(data_len == 20):
                        data_20 = struct.unpack('!20B',recv_msg)
                        # print(data_20[11])



                    self.Run_Count = self.Run_Count + 1
                    send_str = 'send count:{0}'.format(self.Run_Count)

                    self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, fy_angle, xh_angle)
                    # # print("<<"+str(recv_addr[0]))
                    # print(self.Run_Count)
                time.sleep(0.01) 
            except Exception as e:
                pass