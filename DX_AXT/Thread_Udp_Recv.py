
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import struct

class Thread_Udp_Recv(QThread):

    DX_Thread_OutSingal = pyqtSignal(str, int, float, float, str, dict)

    def __init__(self, socket, parent = None):
        super(Thread_Udp_Recv, self).__init__(parent)
        self.working_flag = False
        self.Run_Count = 0
        self.socket = socket
        # print('thread init')


    # 线程运行控制
    def setRun(self):
        temp = {}
        if(self.working_flag == False):
            print("recv------->true")
            self.working_flag = True
            self.DX_Thread_OutSingal.emit('thread set run', 1, 0, 0, 'recv_run', temp)

        elif(self.working_flag == True):
            print("recv------->false")
            self.working_flag = False
            self.Run_Count = 0
            self.DX_Thread_OutSingal.emit('thread set stop', 0, 0, 0, 'recv_stop', temp)


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
                    # 每条网络转发的CAN报文Size为13Byte-7条CAN报文Size为91Bytes
                    if(data_len == 91):
                        
                        pro_data = []
                        pro_data_dict = {}
                        mid_index = 4
                        data_start_index = 5
                        data_end_index = 13
                        data_13 = struct.unpack('!91B',recv_msg)
                        # - 真实91Bytes
                        # 88 08 00 24 07 A9 B0 20 FF D9 37 00 00 
                        # 88 08 00 24 06 DA 00 DA FD D7 FD 00 2D 
                        # 88 08 00 24 05 00 58 0E 00 00 00 00 A1 
                        # 88 08 00 24 04 00 00 00 00 00 00 00 00 
                        # 88 08 00 24 03 00 00 02 E6 C5 CE 00 00 
                        # 88 08 00 24 02 2B 80 2C 03 00 01 06 41 
                        # 88 08 00 24 01 00 0B 41 F0 3C 00 00 00 

                        # pyuic5 -o ui_dx_new.py ui_dx_new.ui ----------->

                        # -报文1-
                        # -ID段
                        id_byte1 = data_13[1]
                        id_byte2 = data_13[2]
                        RID = ((data_13[3] & 0xf0) >> 4)
                        SID = (data_13[3] & 0x0f)

                        MID = data_13[mid_index]
                        # -数据段第1字节
                        data_byte1 = data_13[5]
                        data_byte2 = data_13[6]
                        data_byte3 = data_13[7]
                        data_byte4 = data_13[8]
                        data_byte5 = data_13[9]
                        data_byte6 = data_13[10]
                        data_byte7 = data_13[11]
                        data_byte8 = data_13[12]

                        # - ID为7报文处理
                        pro_data.append(data_13[mid_index])
                        for x in range(data_start_index,data_end_index):
                            pro_data.append(data_13[x])
                        # -数据处理
                        AXT_CAN_Data_Pro(self, pro_data, pro_data_dict)
                        pro_data.clear()

                        mid_index = 4 + 13
                        data_start_index = 5 + 13
                        data_end_index = 13 + 13
                        # - ID为6报文处理
                        pro_data.append(data_13[mid_index])
                        for x in range(data_start_index,data_end_index):
                            pro_data.append(data_13[x])
                        # -数据处理
                        AXT_CAN_Data_Pro(self, pro_data, pro_data_dict)
                        pro_data.clear()

                        mid_index = 4 + 13 + 13
                        data_start_index = 5 + 13 + 13
                        data_end_index = 13 + 13 + 13
                        # - ID为5报文处理
                        pro_data.append(data_13[mid_index])
                        for x in range(data_start_index,data_end_index):
                            pro_data.append(data_13[x])
                        # -数据处理
                        AXT_CAN_Data_Pro(self, pro_data, pro_data_dict)
                        pro_data.clear()

                        mid_index = 4 + 13 + 13 + 13
                        data_start_index = 5 + 13 + 13 + 13
                        data_end_index = 13 + 13 + 13 + 13
                        # - ID为4报文处理
                        pro_data.append(data_13[mid_index])
                        for x in range(data_start_index,data_end_index):
                            pro_data.append(data_13[x])
                        # -数据处理
                        AXT_CAN_Data_Pro(self, pro_data, pro_data_dict)
                        pro_data.clear()

                        mid_index = 4 + 13 + 13 + 13 + 13
                        data_start_index = 5 + 13 + 13 + 13 + 13
                        data_end_index = 13 + 13 + 13 + 13 + 13
                        # - ID为3报文处理
                        pro_data.append(data_13[mid_index])
                        for x in range(data_start_index,data_end_index):
                            pro_data.append(data_13[x])
                        # -数据处理
                        AXT_CAN_Data_Pro(self, pro_data, pro_data_dict)
                        pro_data.clear()

                        mid_index = 4 + 13 + 13 + 13 + 13 + 13
                        data_start_index = 5 + 13 + 13 + 13 + 13 + 13
                        data_end_index = 13 + 13 + 13 + 13 + 13 + 13
                        # - ID为2报文处理
                        pro_data.append(data_13[mid_index])
                        for x in range(data_start_index,data_end_index):
                            pro_data.append(data_13[x])
                        # -数据处理
                        AXT_CAN_Data_Pro(self, pro_data, pro_data_dict)
                        pro_data.clear()

                        mid_index = 4 + 13 + 13 + 13 + 13 + 13 + 13
                        data_start_index = 5 + 13 + 13 + 13 + 13 + 13 + 13
                        data_end_index = 13 + 13 + 13 + 13 + 13 + 13 + 13
                        # - ID为1报文处理
                        pro_data.append(data_13[mid_index])
                        for x in range(data_start_index,data_end_index):
                            pro_data.append(data_13[x])
                        # -数据处理
                        AXT_CAN_Data_Pro(self, pro_data, pro_data_dict)
                        pro_data.clear()
                        
                        # print(pro_data_dict)

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

                    self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, 0, 0, send_str, pro_data_dict)
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



def AXT_CAN_Data_Pro(self, data_pro, pro_data_dict):
    # print(data_pro)
    # -工作状态报文
    if(data_pro[0] == 1):
        # -各管Bomb在位信息
        # AXT_Tube1_BombStatus =  data_pro[1] & 0x01
        # AXT_Tube2_BombStatus = (data_pro[1] & 0x02) >> 1
        # AXT_Tube3_BombStatus = (data_pro[1] & 0x04) >> 2
        # AXT_Tube4_BombStatus = (data_pro[1] & 0x08) >> 3
        # AXT_Tube5_BombStatus = (data_pro[1] & 0x10) >> 4
        # AXT_Tube6_BombStatus = (data_pro[1] & 0x20) >> 5
        pro_data_dict["AXT_Tube1_BombStatus"] = data_pro[1] & 0x01
        pro_data_dict["AXT_Tube2_BombStatus"] = (data_pro[1] & 0x02) >> 1
        pro_data_dict["AXT_Tube3_BombStatus"] = (data_pro[1] & 0x04) >> 2
        pro_data_dict["AXT_Tube4_BombStatus"] = (data_pro[1] & 0x08) >> 3
        pro_data_dict["AXT_Tube5_BombStatus"] = (data_pro[1] & 0x10) >> 4
        pro_data_dict["AXT_Tube6_BombStatus"] = (data_pro[1] & 0x20) >> 5

        # - 充气及驱动机柜状态
        AXT_DevPart1_Status = data_pro[2] & 0x01
        # - 发射管及驱动机构状态
        AXT_DevPart2_Status = data_pro[4] & 0x01
        # - 各管电缆回插状态
        AXT_Tube1_CableStatus =  data_pro[6] & 0x01
        AXT_Tube2_CableStatus = (data_pro[6] & 0x02) >> 1
        AXT_Tube3_CableStatus = (data_pro[6] & 0x04) >> 2
        AXT_Tube4_CableStatus = (data_pro[6] & 0x08) >> 3
        AXT_Tube5_CableStatus = (data_pro[6] & 0x10) >> 4
        AXT_Tube6_CableStatus = (data_pro[6] & 0x20) >> 5
    # -装置反馈报文
    elif(data_pro[0] == 2):
        # - 各管前盖状态
        AXT_Tube1_FrontCaseStatus =  data_pro[1] & 0x07
        AXT_Tube2_FrontCaseStatus = (data_pro[1] & 0x38) >> 3
        AXT_Tube3_FrontCaseStatus = ((data_pro[1] & 0xC0) >> 6) | ((data_pro[2] & 0x01) << 2)
        AXT_Tube4_FrontCaseStatus = (data_pro[2] & 0x0E) >> 1
        AXT_Tube5_FrontCaseStatus = (data_pro[2] & 0x70) >> 4
        AXT_Tube6_FrontCaseStatus = ((data_pro[2] & 0x80) >> 7) | ((data_pro[3] & 0x03) << 1)
        # - 各管前盖反馈状态有效标志
        # - FY角度
        # - XH角度
    # -发射命令反馈报文
    elif(data_pro[0] == 3):
        # - 各管发射命令反馈
        AXT_Tube1_FireConfirm_EN = data_pro[1] & 0x01
        AXT_Tube1_FireInfo =      (data_pro[1] & 0x0E) >> 1
        AXT_Tube1_FireErrInfo =   (data_pro[1] & 0xF0) >> 4
        AXT_Tube2_FireConfirm_EN = data_pro[2] & 0x01
        AXT_Tube2_FireInfo =      (data_pro[2] & 0x0E) >> 1
        AXT_Tube2_FireErrInfo =   (data_pro[2] & 0xF0) >> 4
        AXT_Tube3_FireConfirm_EN = data_pro[3] & 0x01
        AXT_Tube3_FireInfo =      (data_pro[3] & 0x0E) >> 1
        AXT_Tube3_FireErrInfo =   (data_pro[3] & 0xF0) >> 4
        AXT_Tube4_FireConfirm_EN = data_pro[4] & 0x01
        AXT_Tube4_FireInfo =      (data_pro[4] & 0x0E) >> 1
        AXT_Tube4_FireErrInfo =   (data_pro[4] & 0xF0) >> 4
        AXT_Tube5_FireConfirm_EN = data_pro[5] & 0x01
        AXT_Tube5_FireInfo =      (data_pro[5] & 0x0E) >> 1
        AXT_Tube5_FireErrInfo =   (data_pro[5] & 0xF0) >> 4
        AXT_Tube6_FireConfirm_EN = data_pro[6] & 0x01
        AXT_Tube6_FireInfo =      (data_pro[6] & 0x0E) >> 1
        AXT_Tube6_FireErrInfo =   (data_pro[6] & 0xF0) >> 4
    # -关机报文
    elif(data_pro[0] == 4):
        AXT_Dev_Close  = 0x01
    # -各管气压报文
    elif(data_pro[0] == 5):
        AXT_Dev_AirPressure =   data_pro[1]
        AXT_Tube1_AirPressure = data_pro[2]
        AXT_Tube2_AirPressure = data_pro[3]
        AXT_Tube3_AirPressure = data_pro[4]
        AXT_Tube4_AirPressure = data_pro[5]
        AXT_Tube5_AirPressure = data_pro[6]
        AXT_Tube6_AirPressure = data_pro[7]
    # -各管温度报文(1~3号管)
    elif(data_pro[0] == 6):
        # 88 08 00 24 06 ----> DA 00 DA FD D7 FD 00 2D 
        # print(data_pro)
        AXT_Tube1_Warm_Status =  data_pro[1] & 0x01
        AXT_Tube2_Warm_Status = (data_pro[1] & 0x02) >> 1
        AXT_Tube3_Warm_Status = (data_pro[1] & 0x04) >> 2
        AXT_Tube4_Warm_Status = (data_pro[1] & 0x08) >> 3
        AXT_Tube5_Warm_Status = (data_pro[1] & 0x10) >> 4
        AXT_Tube6_Warm_Status = (data_pro[1] & 0x20) >> 5
        # AXT_Tube1_Temperature = (((data_pro[2] << 8) | data_pro[3]) * 0.1)
        # AXT_Tube2_Temperature = (((data_pro[4] << 8) | data_pro[5]) * 0.1)
        # AXT_Tube3_Temperature = (((data_pro[6] << 8) | data_pro[7]) * 0.1)
        # print(AXT_Tube2_Temperture)
        pro_data_dict["AXT_Tube1_Temperature"] = (((data_pro[3] << 8) | data_pro[2]) * 0.1)
        pro_data_dict["AXT_Tube2_Temperature"] = (((data_pro[5] << 8) | data_pro[4]) * 0.1)
        pro_data_dict["AXT_Tube3_Temperature"] = (((data_pro[7] << 8) | data_pro[6]) * 0.1)
    # -各管温度报文(4~6号管)
    elif(data_pro[0] == 7):
        # print(data_pro)
        # AXT_Tube4_Temperature = (((data_pro[1] << 8) | data_pro[2]) * 0.1)
        # AXT_Tube5_Temperature = (((data_pro[3] << 8) | data_pro[4]) * 0.1)
        # AXT_Tube6_Temperature = (((data_pro[5] << 8) | data_pro[6]) * 0.1)
        # print(AXT_Tube4_Temperture)
        pro_data_dict["AXT_Tube4_Temperature"] = (((data_pro[2] << 8) | data_pro[1]) * 0.1)
        pro_data_dict["AXT_Tube5_Temperature"] = (((data_pro[4] << 8) | data_pro[3]) * 0.1)
        pro_data_dict["AXT_Tube6_Temperature"] = (((data_pro[6] << 8) | data_pro[5]) * 0.1)
        

