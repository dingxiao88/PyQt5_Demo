
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import struct

class Thread_Udp_Recv(QThread):

    DX_Thread_OutSingal = pyqtSignal(str, int, float, float, str)

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
            self.DX_Thread_OutSingal.emit('thread set run', 1, 0, 0, 'recv_run')

        elif(self.working_flag == True):
            self.working_flag = False
            self.Run_Count = 0
            self.DX_Thread_OutSingal.emit('thread set stop', 0, 0, 0, 'recv_stop')


    # 线程运行主循环
    def run(self):
        while(self.working_flag == True):
            try:
                # # receiveData = udpSocket.recvfrom(1024)
                # recv_msg, recv_addr = self.socket.recvfrom(1024)
                # # print("<<%s:%s"%(str(receiveData[1]),str(receiveData[0]))) 
                # # print("<<"+str(recv_addr[1]))
                # if((str(recv_addr[0]) == "192.168.10.40") and (str(recv_addr[1]) == "21785")):
                # # if((str(recv_addr[0]) == "192.168.0.106") or (str(recv_addr[0]) == "192.168.31.79") or (str(recv_addr[0]) == "10.0.0.24")):

                #     # msg1 = struct.unpack('!18B',recv_msg)  #!网络字节顺序 20字节 B unsigned char
                #     # print(msg1[15])

                #     # 接收到的数据长度
                #     # print(str(len(recv_msg)))

                #     # msg = recv_msg.decode('utf-8')
                #     # # msg = '来自IP:{}端口:{}:\n{}\n'.format(recv_addr[0], recv_addr[1], msg)
                #     # msg = '来自IP:{}端口:{}:\n'.format(recv_addr[0], recv_addr[1])
                #     # print(msg)

                #     data_len = len(recv_msg)

                #     # 数据报文20B-随动角度报文
                #     if(data_len == 20):
                #         data_18 = struct.unpack('!20B',recv_msg)
                #         # //@-MK3设备-FY输入角度
                #         # temp1 = (int)(Computer_NetRecv_Data[13]&0xff);
                #         # temp2 = (int)(Computer_NetRecv_Data[12]&0xff);
                #         # temp3 = (int)((temp1*256)+temp2);
                #         # if(temp1>=128)
                #         # {
                #         # temp3 = (temp3 - 65535) - 1;
                #         # }
                #         # MK3_FY_InputAngle = (float)((temp3*180)/16384.0);

                #         # 俯仰角度 [fff7] -> -0.09
                #         temp_fy_angle = (data_18[14] * 256) + data_18[15]
                #         if(data_18[14] > 128):
                #             temp_fy_angle = temp_fy_angle - 65536
                #         fy_angle = ((temp_fy_angle*180)/16384.0)
                #         fy_angle = round(fy_angle, 2)
                #         # print(fy_angle)
                #         # 0.19775390625

                #         # 旋回角度 [e001] -> -89.98
                #         temp_xh_angle = (data_18[16] * 256) + data_18[17]
                #         if(data_18[16] > 128):
                #             temp_xh_angle = temp_xh_angle - 65536
                #         xh_angle = ((temp_xh_angle*180)/16384.0)
                #         xh_angle = round(xh_angle, 2)
                #         # print(xh_angle) 
                #         # -91.95556640625

                #     # 数据报文20B-随动状态报文
                #     elif(data_len == 20):
                #         data_20 = struct.unpack('!20B',recv_msg)
                #         # print(data_20[11])



                #     self.Run_Count = self.Run_Count + 1
                #     send_str = 'send count:{0}'.format(self.Run_Count)

                #     self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, fy_angle, xh_angle)
                #     # # print("<<"+str(recv_addr[0]))
                #     # print(self.Run_Count)


                #--------------------------------------AXT 双CAN模块------------------------------------------------
                recv_msg, recv_addr = self.socket.recvfrom(1024)
                # print("<<%s:%s"%(str(receiveData[1]),str(receiveData[0]))) 
                # print("<<"+str(recv_addr[0]))
                if((str(recv_addr[0]) == "192.168.0.19") and (str(recv_addr[1]) == "6000")):
                # if((str(recv_addr[0]) == "192.168.0.106") or (str(recv_addr[0]) == "192.168.31.79") or (str(recv_addr[0]) == "10.0.0.24")):

                    # msg1 = struct.unpack('!18B',recv_msg)  #!网络字节顺序 20字节 B unsigned char
                    # print(msg1[15])

                    # 接收到的数据长度
                    # print(str(len(recv_msg)))

                    # msg = recv_msg.decode('utf-8')
                    # # msg = '来自IP:{}端口:{}:\n{}\n'.format(recv_addr[0], recv_addr[1], msg)
                    # msg = '--->IP:{}--->Port:{}:\n'.format(recv_addr[0], recv_addr[1])
                    # print(msg)

                    data_len = len(recv_msg)
                    # print(data_len)

                    # 数据报文13B-CAN报文-扩展帧-数据帧
                    if(data_len == 91):
                        data_13 = struct.unpack('!91B',recv_msg)

                        # pyuic5 -o ui_dx_new.py ui_dx_new.ui ----------->

                        # -ID段
                        id_byte1 = data_13[1]
                        id_byte2 = data_13[2]
                        RID = ((data_13[3] & 0xf0) >> 4)
                        SID = (data_13[3] & 0x0f)
                        MID = data_13[4]

                        # -数据段第1字节
                        data_byte1 = data_13[5]
                        data_byte2 = data_13[6]
                        data_byte3 = data_13[7]
                        data_byte4 = data_13[8]
                        data_byte5 = data_13[9]
                        data_byte6 = data_13[10]
                        data_byte7 = data_13[11]
                        data_byte8 = data_13[12]

                        


                        # //@-MK3设备-FY输入角度
                        # temp1 = (int)(Computer_NetRecv_Data[13]&0xff);
                        # temp2 = (int)(Computer_NetRecv_Data[12]&0xff);
                        # temp3 = (int)((temp1*256)+temp2);
                        # if(temp1>=128)
                        # {
                        # temp3 = (temp3 - 65535) - 1;
                        # }
                        # MK3_FY_InputAngle = (float)((temp3*180)/16384.0);

                        # # 俯仰角度 [fff7] -> -0.09
                        # temp_fy_angle = (data_18[14] * 256) + data_18[15]
                        # if(data_18[14] > 128):
                        #     temp_fy_angle = temp_fy_angle - 65536
                        # fy_angle = ((temp_fy_angle*180)/16384.0)
                        # fy_angle = round(fy_angle, 2)
                        # # print(fy_angle)
                        # # 0.19775390625

                        # # 旋回角度 [e001] -> -89.98
                        # temp_xh_angle = (data_18[16] * 256) + data_18[17]
                        # if(data_18[16] > 128):
                        #     temp_xh_angle = temp_xh_angle - 65536
                        # xh_angle = ((temp_xh_angle*180)/16384.0)
                        # xh_angle = round(xh_angle, 2)
                        # # print(xh_angle) 
                        # # -91.95556640625

                    self.Run_Count = self.Run_Count + 1
                    send_str = 'Recv_count:{0} -- RID:{1} -- SID:{2} -- MID:{3} -- DATA:{4}-{5}-{6}-{7}-{8}-{9}-{10}-{11}'.format(self.Run_Count, RID, SID, MID, 
                    data_byte1, data_byte2, data_byte3, data_byte4, data_byte5, data_byte6, data_byte7, data_byte8)
                    # print(self.Run_Count)

                    self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, 0, 0, send_str)
                    # self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, fy_angle, xh_angle)
                    # # print("<<"+str(recv_addr[0]))
                    # print(self.Run_Count)


                elif((str(recv_addr[0]) == "192.168.0.107") and (str(recv_addr[1]) == "6000")):
                    print("<<"+str(recv_addr[0]))

                elif((str(recv_addr[0]) == "192.168.0.109") and (str(recv_addr[1]) == "6001")):
                    print("<<"+str(recv_addr[0]))


                time.sleep(0.01) 
            except Exception as e:
                pass