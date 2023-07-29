
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import struct

class Thread_Udp_Recv(QThread):

    DX_Thread_OutSingal = pyqtSignal(str, int, float, float, str, dict, int)

    def __init__(self, socket, parent = None):
        super(Thread_Udp_Recv, self).__init__(parent)
        self.working_flag = False
        self.Run_Count = 0
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.count5 = 0
        self.count6 = 0
        self.count7 = 0
        self.socket = socket
        # print('thread init')

        self.tube4_heat_flag = 0
        self.tube5_heat_flag = 0
        self.tube6_heat_flag = 0


    # 线程运行控制
    def setRun(self):
        temp = {}
        if(self.working_flag == False):
            print("recv------->true")
            self.working_flag = True
            self.DX_Thread_OutSingal.emit('thread set run', 1, 0, 0, 'recv_run', temp, 0)

        elif(self.working_flag == True):
            print("recv------->false")
            self.working_flag = False
            self.Run_Count = 0
            self.DX_Thread_OutSingal.emit('thread set stop', 0, 0, 0, 'recv_stop', temp, 0)


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
                    # 每条网络转发的CAN报文Size为13Byte-20221218
                    if(data_len == 13):
                        # AXT双CAN模块转发CAN数据-20230130-------->
                        data_13 = struct.unpack('!13B',recv_msg)
                        # print("----->13")
                        AXT_CAN_RecvData_Pro(self, data_13, 1)

                        # msg = '--->Data:{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}\n'.format(data_13[0], data_13[1], data_13[2], data_13[3]
                        #                                                                  , data_13[4], data_13[5], data_13[6], data_13[7]
                        #                                                                  , data_13[8], data_13[9], data_13[10], data_13[11]
                        #                                                                  , data_13[12])
                        # print(msg)

                        # pro_data = []
                        # mid_index = 4
                        # data_start_index = 5
                        # data_end_index = 13

                        # # AXT双CAN模块转发CAN数据-20221218-------->
                        # data_13 = struct.unpack('!13B',recv_msg)

                        # # pyuic5 -o ui_dx_new.py ui_dx_new.ui ----------->

                        # # -报文-
                        # # -ID段
                        # id_byte1 = data_13[1]
                        # id_byte2 = data_13[2]
                        # RID = ((data_13[3] & 0xf0) >> 4)
                        # SID = (data_13[3] & 0x0f)

                        # MID = data_13[mid_index]
                        # # -数据段第1字节
                        # data_byte1 = data_13[5]
                        # data_byte2 = data_13[6]
                        # data_byte3 = data_13[7]
                        # data_byte4 = data_13[8]
                        # data_byte5 = data_13[9]
                        # data_byte6 = data_13[10]
                        # data_byte7 = data_13[11]
                        # data_byte8 = data_13[12]


                        # # 处理AXT双CAN模块转发CAN数据-20221218-------->
                        # # 判断RID SID 及CAN帧类型
                        # if(RID == 2 and SID == 4):
                        #     # 判断报文ID
                        #     if((MID == 1) or (MID == 2) or(MID == 3) or(MID == 4) or(MID == 5) or(MID == 6) or(MID == 7)):

                        #         # 报文计数
                        #         if(MID == 1):
                        #             self.count1 = self.count1 + 1
                        #         elif(MID == 2):
                        #             self.count2 = self.count2 + 1
                        #         elif(MID == 3):
                        #             self.count3 = self.count3 + 1
                        #         elif(MID == 4):
                        #             self.count4 = self.count4 + 1
                        #         elif(MID == 5):
                        #             self.count5 = self.count5 + 1
                        #         elif(MID == 6):
                        #             self.count6 = self.count6 + 1
                        #         elif(MID == 7):
                        #             self.count7 = self.count7 + 1            
                                
                        #         # 数据处理
                        #         pro_data.append(data_13[mid_index])
                        #         for x in range(data_start_index,data_end_index):
                        #             pro_data.append(data_13[x])
                        #         # -数据处理
                        #         pro_data_dict = AXT_CAN_Data_Pro(pro_data)
                        #         pro_data.clear()

                        #         # 组合数据
                        #         self.Run_Count = self.Run_Count + 1
                        #         # send_str = 'Recv_count:{0}--RID:{1}--SID:{2}--MID:{3}--DATA:{4}-{5}-{6}-{7}-{8}-{9}-{10}-{11}--C:D1[{12}]-D2[{13}]-D3[{14}]-D4[{15}]-D5[{16}]-D6[{17}]-D7[{18}]'.format(self.Run_Count, RID, SID, MID, 
                        #         # data_byte1, data_byte2, data_byte3, data_byte4, data_byte5, data_byte6, data_byte7, data_byte8, self.count1, self.count2, self.count3, self.count4, self.count5, self.count6, self.count7)
                        #         send_str = 'Recv_count:{0}--RID:{1}--SID:{2}--MID:{3}--C:D1[{4}]-D2[{5}]-D3[{6}]-D4[{7}]-D5[{8}]-D6[{9}]-D7[{10}]'.format(self.Run_Count, RID, SID, MID, 
                        #         self.count1, self.count2, self.count3, self.count4, self.count5, self.count6, self.count7)
                        #         # 发送显示数据
                        #         self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, 0, 0, send_str, pro_data_dict, MID)
                    
                    if(data_len == 26):  # 2帧数据同时打包
                        # AXT双CAN模块转发CAN数据-20230130-------->
                        data_26 = struct.unpack('!26B',recv_msg)
                        # print("----->26")
                        AXT_CAN_RecvData_Pro(self, data_26, 2)

                    if(data_len == 39):  # 3帧数据同时打包
                        # AXT双CAN模块转发CAN数据-20230130-------->
                        data_39 = struct.unpack('!39B',recv_msg)
                        # print("----->39")
                        AXT_CAN_RecvData_Pro(self, data_39, 3)

                    if(data_len == 52):  # 4帧数据同时打包
                        # AXT双CAN模块转发CAN数据-20230130-------->
                        data_52 = struct.unpack('!52B',recv_msg)
                        # print("----->52")
                        AXT_CAN_RecvData_Pro(self, data_52, 4)

                    # 防止CAN模块打包数据-应对CAN模块同时打包5,6,7帧数据
                    if(data_len == 65):  # 5帧数据同时打包

                        # AXT双CAN模块转发CAN数据-20221219-------->
                        data_65 = struct.unpack('!65B',recv_msg)
                        # print("----->65")
                        AXT_CAN_RecvData_Pro(self, data_65, 5)

                    if(data_len == 78):  # 6帧数据同时打包
                        # AXT双CAN模块转发CAN数据-20230130-------->
                        data_78 = struct.unpack('!78B',recv_msg)
                        # print("----->78")
                        AXT_CAN_RecvData_Pro(self, data_78, 6)

                    if(data_len == 91):  # 7帧数据同时打包
                        # AXT双CAN模块转发CAN数据-20230130-------->
                        data_91 = struct.unpack('!91B',recv_msg)
                        # print("----->91")
                        AXT_CAN_RecvData_Pro(self, data_91, 7)

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

                    # -----------------------以下20221218注释掉------------------
                    # self.Run_Count = self.Run_Count + 1
                    # send_str = 'Recv_count:{0} -- RID:{1} -- SID:{2} -- MID:{3} -- DATA:{4}-{5}-{6}-{7}-{8}-{9}-{10}-{11}'.format(self.Run_Count, RID, SID, MID, 
                    # data_byte1, data_byte2, data_byte3, data_byte4, data_byte5, data_byte6, data_byte7, data_byte8)
                    # # print(self.Run_Count)

                    # self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, 0, 0, send_str, pro_data_dict)
                    # # self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, fy_angle, xh_angle)
                    # # # print("<<"+str(recv_addr[0]))
                    # # print(self.Run_Count)


                # elif((str(recv_addr[0]) == "192.168.0.107") and (str(recv_addr[1]) == "6000")):
                #     print("<<"+str(recv_addr[0]))

                # elif((str(recv_addr[0]) == "192.168.0.109") and (str(recv_addr[1]) == "6001")):
                #     print("<<"+str(recv_addr[0]))


                time.sleep(0.01) 
            except Exception as e:
                pass


# 双CAN模块接收到的数据处理  
# data_pro:待处理的数据
# info_nums：包含几条打包数据
# self: 非常重要的参数
def AXT_CAN_RecvData_Pro(self, data_pro, info_nums):
    # print(data_pro)
    # print(info_nums)

    # 处理info_nums数据
    for info_index in range(0,(info_nums)):
        
        # ---------初始化--------
        id_start1_index = 1 + (info_index * 13)
        id_start2_index = 2 + (info_index * 13)
        rsid_index = 3 + (info_index * 13)
        mid_index = 4 + (info_index * 13)
        # id_start1_index = 4 + (info_index * 13)
        # id_start2_index = 3 + (info_index * 13)
        # rsid_index = 2 + (info_index * 13)
        # mid_index = 1 + (info_index * 13)
        data_start_index = 5 + (info_index * 13)
        data_end_index = 13 + (info_index * 13)
        # -ID段
        id_byte1 = data_pro[id_start1_index]
        id_byte2 = data_pro[id_start2_index]
        RID = ((data_pro[rsid_index] & 0xf0) >> 4)
        SID = (data_pro[rsid_index] & 0x0f)
        MID = data_pro[mid_index]
        # print(RID)
        # print(SID)
        # print(MID)
        # -数据段第1字节
        data_byte1 = data_pro[mid_index + 1]
        data_byte2 = data_pro[mid_index + 2]
        data_byte3 = data_pro[mid_index + 3]
        data_byte4 = data_pro[mid_index + 4]
        data_byte5 = data_pro[mid_index + 5]
        data_byte6 = data_pro[mid_index + 6]
        data_byte7 = data_pro[mid_index + 7]
        data_byte8 = data_pro[mid_index + 8]

        # print(MID)
        # 判断RID SID 及CAN帧类型
        if(RID == 2 and SID == 4):
            # 判断报文ID
            if((MID == 1) or (MID == 2) or(MID == 3) or(MID == 4) or(MID == 5) or(MID == 6) or(MID == 7)):
                # 报文计数
                if(MID == 1):
                    self.count1 = self.count1 + 1
                elif(MID == 2):
                    self.count2 = self.count2 + 1
                elif(MID == 3):
                    self.count3 = self.count3 + 1
                elif(MID == 4):
                    self.count4 = self.count4 + 1
                elif(MID == 5):
                    self.count5 = self.count5 + 1
                elif(MID == 6):
                    self.count6 = self.count6 + 1
                elif(MID == 7):
                    self.count7 = self.count7 + 1            
                # 数据处理
                pro_data = []
                pro_data.append(data_pro[mid_index])
                for x in range(data_start_index,data_end_index):
                    pro_data.append(data_pro[x])
                # print(pro_data)
                # -数据处理
                pro_data_dict = AXT_CAN_Data_Pro(self, pro_data)
                # print(pro_data_dict)
                pro_data.clear()

                # 组合数据
                self.Run_Count = self.Run_Count + 1
                # send_str = 'Recv_count:{0}--RID:{1}--SID:{2}--MID:{3}--DATA:{4}-{5}-{6}-{7}-{8}-{9}-{10}-{11}--C:D1[{12}]-D2[{13}]-D3[{14}]-D4[{15}]-D5[{16}]-D6[{17}]-D7[{18}]'.format(self.Run_Count, RID, SID, MID, 
                # data_byte1, data_byte2, data_byte3, data_byte4, data_byte5, data_byte6, data_byte7, data_byte8, self.count1, self.count2, self.count3, self.count4, self.count5, self.count6, self.count7)
                send_str = 'Recv_count:{0}--RID:{1}--SID:{2}--MID:{3}--C:D1[{4}]-D2[{5}]-D3[{6}]-D4[{7}]-D5[{8}]-D6[{9}]-D7[{10}]'.format(self.Run_Count, RID, SID, MID, 
                self.count1, self.count2, self.count3, self.count4, self.count5, self.count6, self.count7)
                # 发送显示数据
                self.DX_Thread_OutSingal.emit(send_str, self.Run_Count, 0, 0, send_str, pro_data_dict, MID)

    # print("AXT_CAN_RecvData_Pro------------>return")
    # return pro_data_dict1


def AXT_CAN_Data_Pro(self, data_pro):

    pro_data_dict = {}

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

        # -AXT设备工作状态
        pro_data_dict["AXT_Dev_Status"] = data_pro[2]

        # -AXT设备故障ID
        pro_data_dict["AXT_Dev_ErrorID"] = data_pro[3]

        # -AXT设备母线状态
        pro_data_dict["AXT_Dev_MainPower_Status"] = data_pro[4] & 0x01

        # -AXT设备FY运行状态
        pro_data_dict["AXT_Dev_FY_Status"] = (data_pro[4] & 0x02) >> 1

        # -AXT设备XH运行状态
        pro_data_dict["AXT_Dev_XH_Status"] = (data_pro[4] & 0x04) >> 2

        # -AXT设备各管电缆回插状态
        pro_data_dict["AXT_Tube1_CableStatus"] = data_pro[6] & 0x01
        pro_data_dict["AXT_Tube2_CableStatus"] = (data_pro[6] & 0x02) >> 1
        pro_data_dict["AXT_Tube3_CableStatus"] = (data_pro[6] & 0x04) >> 2
        pro_data_dict["AXT_Tube4_CableStatus"] = (data_pro[6] & 0x08) >> 3
        pro_data_dict["AXT_Tube5_CableStatus"] = (data_pro[6] & 0x10) >> 4
        pro_data_dict["AXT_Tube6_CableStatus"] = (data_pro[6] & 0x20) >> 5

        # temp6 = (data_pro[1] & 0x20) >> 5
        # print(temp6)

        # - 充气及驱动机柜状态
        AXT_DevPart1_Status = data_pro[2] & 0x01
        # - 发射管及驱动机构状态
        AXT_DevPart2_Status = data_pro[4] & 0x01
        # # - 各管电缆回插状态
        # AXT_Tube1_CableStatus =  data_pro[6] & 0x01
        # AXT_Tube2_CableStatus = (data_pro[6] & 0x02) >> 1
        # AXT_Tube3_CableStatus = (data_pro[6] & 0x04) >> 2
        # AXT_Tube4_CableStatus = (data_pro[6] & 0x08) >> 3
        # AXT_Tube5_CableStatus = (data_pro[6] & 0x10) >> 4
        # AXT_Tube6_CableStatus = (data_pro[6] & 0x20) >> 5
    # -装置反馈报文
    elif(data_pro[0] == 2):
        # - 各管前盖状态
        # AXT_Tube1_FrontCaseStatus =  data_pro[1] & 0x07
        # AXT_Tube2_FrontCaseStatus = (data_pro[1] & 0x38) >> 3
        # AXT_Tube3_FrontCaseStatus = ((data_pro[1] & 0xC0) >> 6) | ((data_pro[2] & 0x01) << 2)
        # AXT_Tube4_FrontCaseStatus = (data_pro[2] & 0x0E) >> 1
        # AXT_Tube5_FrontCaseStatus = (data_pro[2] & 0x70) >> 4
        # AXT_Tube6_FrontCaseStatus = ((data_pro[2] & 0x80) >> 7) | ((data_pro[3] & 0x03) << 1)
        pro_data_dict["AXT_Tube1_FrontCaseStatus"] =  data_pro[1] & 0x07
        pro_data_dict["AXT_Tube2_FrontCaseStatus"] = (data_pro[1] & 0x38) >> 3
        pro_data_dict["AXT_Tube3_FrontCaseStatus"] = ((data_pro[1] & 0xC0) >> 6) | ((data_pro[2] & 0x01) << 2)
        pro_data_dict["AXT_Tube4_FrontCaseStatus"] = (data_pro[2] & 0x0E) >> 1
        pro_data_dict["AXT_Tube5_FrontCaseStatus"] = (data_pro[2] & 0x70) >> 4
        pro_data_dict["AXT_Tube6_FrontCaseStatus"] = ((data_pro[2] & 0x80) >> 7) | ((data_pro[3] & 0x03) << 1)
        # print(data_pro[1])
        # - 各管前盖反馈状态有效标志
        # data_pro[4]
        # print(data_pro[4])

        # - XH角度
        # data_pro[5] data_pro[6]
        xh_1 = ((data_pro[5] * 256) + data_pro[6])
        # print('xh_1-0x%x'%xh_1)
        xh_2 = xh_1 & 0xfff0
        xh_en = (xh_1 & 0x0001)
        xh_info = ((xh_1 & 0x000e) >> 1)
        # print(xh_info)
        # print('xh_2-0x%x'%xh_2)
        xh_3 = (xh_2 >> 4) 
        # print('xh_3-[%d]'%xh_3)
        temp_xh_angle = xh_3
        # -符号位
        xxh_2 = ((xh_2 & 0x8000) >> 15)  
        # print(xxh_2)
        if(xxh_2 == 1):
            xh_4 = 0xfff - xh_3 + 1
            # print('xh_4-[%d]'%xh_4)
            temp_xh_angle = 0 - xh_4

        xh_angle = (temp_xh_angle * 0.1)
        xh_angle = round(xh_angle, 2)
        # print(xh_angle) 
        pro_data_dict["AXT_XH_EN"] = xh_en
        pro_data_dict["AXT_XH_Info"] = xh_info
        pro_data_dict["AXT_XH_RealAngle"] = xh_angle

        # - FY角度
        # data_pro[7] data_pro[8]
        fy_1 = ((data_pro[7] * 256) + data_pro[8])
        # print('fy_1-0x%x'%fy_1)
        fy_2 = fy_1 & 0xfff0
        fy_en = (fy_1 & 0x0001)
        fy_info = ((fy_1 & 0x000e) >> 1)
        # print('fy_2-0x%x'%fy_2)
        fy_3 = (fy_2 >> 4) 
        # print('fy_3-[%d]'%fy_3)
        temp_fy_angle = fy_3
        # -符号位
        xfy_2 = ((fy_2 & 0x8000) >> 15)  
        # print(xfy_2)
        if(xfy_2 == 1):
            fy_4 = 0xfff - fy_3 + 1
            # print('fy_4-[%d]'%fy_4)
            temp_fy_angle = 0 - fy_4

        fy_angle = (temp_fy_angle * 0.1)
        fy_angle = round(fy_angle, 2)
        # print(fy_angle) 
        pro_data_dict["AXT_FY_EN"] = fy_en
        pro_data_dict["AXT_FY_Info"] = fy_info
        pro_data_dict["AXT_FY_RealAngle"] = fy_angle 


    # -发射命令反馈报文
    elif(data_pro[0] == 3):
        # - 各管发射命令反馈
        # AXT_Tube1_FireConfirm_EN = data_pro[1] & 0x01
        # AXT_Tube1_FireInfo =      (data_pro[1] & 0x0E) >> 1
        # AXT_Tube1_FireErrInfo =   (data_pro[1] & 0xF0) >> 4

        # AXT_Tube2_FireConfirm_EN = data_pro[2] & 0x01
        # AXT_Tube2_FireInfo =      (data_pro[2] & 0x0E) >> 1
        # AXT_Tube2_FireErrInfo =   (data_pro[2] & 0xF0) >> 4

        # AXT_Tube3_FireConfirm_EN = data_pro[3] & 0x01
        # AXT_Tube3_FireInfo =      (data_pro[3] & 0x0E) >> 1
        # AXT_Tube3_FireErrInfo =   (data_pro[3] & 0xF0) >> 4

        # AXT_Tube4_FireConfirm_EN = data_pro[4] & 0x01
        # AXT_Tube4_FireInfo =      (data_pro[4] & 0x0E) >> 1
        # AXT_Tube4_FireErrInfo =   (data_pro[4] & 0xF0) >> 4

        # AXT_Tube5_FireConfirm_EN = data_pro[5] & 0x01
        # AXT_Tube5_FireInfo =      (data_pro[5] & 0x0E) >> 1
        # AXT_Tube5_FireErrInfo =   (data_pro[5] & 0xF0) >> 4

        # AXT_Tube6_FireConfirm_EN = data_pro[6] & 0x01
        # AXT_Tube6_FireInfo =      (data_pro[6] & 0x0E) >> 1
        # AXT_Tube6_FireErrInfo =   (data_pro[6] & 0xF0) >> 4

        pro_data_dict["AXT_Tube1_FireConfirm_EN"] = data_pro[1] & 0x01
        pro_data_dict["AXT_Tube1_FireInfo"] = (data_pro[1] & 0x0E) >> 1

        pro_data_dict["AXT_Tube2_FireConfirm_EN"] = data_pro[2] & 0x01
        pro_data_dict["AXT_Tube2_FireInfo"] = (data_pro[2] & 0x0E) >> 1

        pro_data_dict["AXT_Tube3_FireConfirm_EN"] = data_pro[3] & 0x01
        pro_data_dict["AXT_Tube3_FireInfo"] = (data_pro[3] & 0x0E) >> 1

        pro_data_dict["AXT_Tube4_FireConfirm_EN"] = data_pro[4] & 0x01
        pro_data_dict["AXT_Tube4_FireInfo"] = (data_pro[4] & 0x0E) >> 1

        pro_data_dict["AXT_Tube5_FireConfirm_EN"] = data_pro[5] & 0x01
        pro_data_dict["AXT_Tube5_FireInfo"] = (data_pro[5] & 0x0E) >> 1

        pro_data_dict["AXT_Tube6_FireConfirm_EN"] = data_pro[6] & 0x01
        pro_data_dict["AXT_Tube6_FireInfo"] = (data_pro[6] & 0x0E) >> 1

        # print(pro_data_dict["AXT_Tube6_FireInfo"])

    # -关机报文
    elif(data_pro[0] == 4):
        AXT_Dev_Close  = 0x01
    # -各管气压报文
    elif(data_pro[0] == 5):
        AXT_Dev_AirPressure =   data_pro[1]
        # AXT_Tube1_AirPressure = data_pro[2]
        # AXT_Tube2_AirPressure = data_pro[3]
        # AXT_Tube3_AirPressure = data_pro[4]
        # AXT_Tube4_AirPressure = data_pro[5]
        # AXT_Tube5_AirPressure = data_pro[6]
        # AXT_Tube6_AirPressure = data_pro[7]

        pro_data_dict["AXT_Tube1_AirPressure"] = (data_pro[2] * 0.1)
        pro_data_dict["AXT_Tube2_AirPressure"] = (data_pro[3] * 0.1)
        pro_data_dict["AXT_Tube3_AirPressure"] = (data_pro[4] * 0.1)
        pro_data_dict["AXT_Tube4_AirPressure"] = (data_pro[5] * 0.1)
        pro_data_dict["AXT_Tube5_AirPressure"] = (data_pro[6] * 0.1)
        pro_data_dict["AXT_Tube6_AirPressure"] = (data_pro[7] * 0.1)
    # -各管温度报文(1~3号管)
    elif(data_pro[0] == 6):
        # 88 08 00 24 06 ----> DA 00 DA FD D7 FD 00 2D 
        # print(data_pro)
        # AXT_Tube1_Warm_Status =  data_pro[1] & 0x01
        # AXT_Tube2_Warm_Status = (data_pro[1] & 0x02) >> 1
        # AXT_Tube3_Warm_Status = (data_pro[1] & 0x04) >> 2
        # AXT_Tube4_Warm_Status = (data_pro[1] & 0x08) >> 3
        # AXT_Tube5_Warm_Status = (data_pro[1] & 0x10) >> 4
        # AXT_Tube6_Warm_Status = (data_pro[1] & 0x20) >> 5
        # AXT_Tube1_Temperature = (((data_pro[2] << 8) | data_pro[3]) * 0.1)
        # AXT_Tube2_Temperature = (((data_pro[4] << 8) | data_pro[5]) * 0.1)
        # AXT_Tube3_Temperature = (((data_pro[6] << 8) | data_pro[7]) * 0.1)
        # print(data_pro[3])

        # AXT 1-6管加热状态
        pro_data_dict["AXT_Tube1_Heat_Flag"] = data_pro[1] & 0x01
        pro_data_dict["AXT_Tube2_Heat_Flag"] = (data_pro[1] & 0x02) >> 1
        pro_data_dict["AXT_Tube3_Heat_Flag"] = (data_pro[1] & 0x04) >> 2
        pro_data_dict["AXT_Tube4_Heat_Flag"] = (data_pro[1] & 0x08) >> 3
        pro_data_dict["AXT_Tube5_Heat_Flag"] = (data_pro[1] & 0x10) >> 4
        pro_data_dict["AXT_Tube6_Heat_Flag"] = (data_pro[1] & 0x20) >> 5


        self.tube4_heat_flag = pro_data_dict["AXT_Tube4_Heat_Flag"]
        self.tube5_heat_flag = pro_data_dict["AXT_Tube5_Heat_Flag"]
        self.tube6_heat_flag = pro_data_dict["AXT_Tube6_Heat_Flag"]

        # AXT_Tube1_Temperature 为负数
        if(data_pro[3] >= 128):
            temp1 = 0 - (65535 - ((data_pro[3] << 8) | data_pro[2]) + 1)
        else:
            temp1 = ((data_pro[3] << 8) | data_pro[2])

        # AXT_Tube2_Temperature 为负数
        if(data_pro[5] >= 128):
            temp2 =0 - (65535 - ((data_pro[5] << 8) | data_pro[4]) + 1)
        else:
            temp2 = ((data_pro[5] << 8) | data_pro[4])

        # AXT_Tube3_Temperature 为负数
        if(data_pro[7] >= 128):
            temp3 = 0 - (65535 - ((data_pro[7] << 8) | data_pro[6]) + 1)
        else:
            temp3 = ((data_pro[7] << 8) | data_pro[6])

        pro_data_dict["AXT_Tube1_Temperature"] = (temp1 * 0.1)
        pro_data_dict["AXT_Tube2_Temperature"] = (temp2 * 0.1)
        pro_data_dict["AXT_Tube3_Temperature"] = (temp3 * 0.1)
    # -各管温度报文(4~6号管)
    elif(data_pro[0] == 7):
        # print(data_pro)
        # AXT_Tube4_Temperature = (((data_pro[1] << 8) | data_pro[2]) * 0.1)
        # AXT_Tube5_Temperature = (((data_pro[3] << 8) | data_pro[4]) * 0.1)
        # AXT_Tube6_Temperature = (((data_pro[5] << 8) | data_pro[6]) * 0.1)
        # print(AXT_Tube4_Temperture)
        # print(data_pro[2])

        pro_data_dict["AXT_Tube4_Heat_Flag"] = self.tube4_heat_flag
        pro_data_dict["AXT_Tube5_Heat_Flag"] = self.tube5_heat_flag
        pro_data_dict["AXT_Tube6_Heat_Flag"] = self.tube6_heat_flag
        
        # AXT_Tube4_Temperature 为负数
        if(data_pro[2] >= 128):
            temp4 = 0 - (65535 - ((data_pro[2] << 8) | data_pro[1]) + 1)
        else:
            temp4 = ((data_pro[2] << 8) | data_pro[1])

        # AXT_Tube5_Temperature 为负数
        if(data_pro[4] >= 128):
            temp5 = 0 - (65535 - ((data_pro[4] << 8) | data_pro[3]) + 1)
        else:
            temp5 = ((data_pro[4] << 8) | data_pro[3])

        # AXT_Tube6_Temperature 为负数
        if(data_pro[6] >= 128):
            temp6 = 0 - (65535 - ((data_pro[6] << 8) | data_pro[5]) + 1)
        else:
            temp6 = ((data_pro[6] << 8) | data_pro[5])

        pro_data_dict["AXT_Tube4_Temperature"] = (temp4 * 0.1)
        pro_data_dict["AXT_Tube5_Temperature"] = (temp5 * 0.1)
        pro_data_dict["AXT_Tube6_Temperature"] = (temp6 * 0.1)
        
    return pro_data_dict

# # 测试
# test_data = [] 
# #AXT双网发送数据初始化
# for x in range(65):
#     test_data.append(0x00)
# AXT_CAN_RecvData_Pro(test_data,5)