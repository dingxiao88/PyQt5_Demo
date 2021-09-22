
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
import os
import requests
import json
import threading
import struct
import time
import psutil
from pathlib import Path
from pyqt_led import Led          # https://github.com/Neur1n/pyqt_led

# 运行外部命令
import subprocess

import shutil

# 颜色识取器
from colorpicker import ColorPicker

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtSvg


# # 引入设计样式
# # https://github.com/ColinDuquesnoy/QDarkStyleSheet
# import qdarkstyle
# # https://github.com/gmarull/qtmodern
# import qtmodern.styles
# import qtmodern.windows


# Meter.py中内容
from Meter import *


defJson = {
    'value_color': '#ffffff',
    'pointer_color': '#ffffff',
    'value_min': 0,
    'value_max': 40, 
    }
write_json = {}


# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        # --------------------------------------------------------------
        # 关闭所有窗口,也不关闭应用程序
        # QApplication.setQuitOnLastWindowClosed(False)
        super(mainWin, self).__init__(parent)
        self.setupUi(self)

        # 读取Config json文件
        file_flag = os.path.exists("./gaguge_config.json")
        # print(file_flag)
        if(file_flag == False):
            with  open('./gaguge_config.json','w',encoding = 'utf-8') as congfig_file:
                json.dump(defJson, congfig_file, indent=4, sort_keys=True)
            with open('./gaguge_config.json', 'r', encoding='utf8') as read_congfig_file:
                str_temp = read_congfig_file.read()
                json_data = json.loads(str_temp)
                self.value_color = json_data['value_color']
                self.pointer_color = json_data['pointer_color']
                self.value_min = json_data['value_min']
                self.value_max = json_data['value_max']
        elif(file_flag ==  True):
            with open('./gaguge_config.json', 'r', encoding='utf8') as read_congfig_file:
                str_temp = read_congfig_file.read()
                json_data = json.loads(str_temp)
                self.value_color = json_data['value_color']
                self.pointer_color = json_data['pointer_color']
                self.value_min = json_data['value_min']
                self.value_max = json_data['value_max']
                # print(self.value_color)

        # 绑定按键响应函数
        # 1 表盘选择
        self.pushButton_gague_choose.clicked.connect(self.Gague_Choose)
        # 2 表盘指针颜色
        self.pushButton_pointer_color.clicked.connect(self.Gague_Pointer_ColorChange)
        # 3 表盘数值颜色
        self.pushButton_value_color.clicked.connect(self.Gague_Value_ColorChange)
        # 4 数值范围(最小值)
        self.pushButton_value_min.clicked.connect(self.Gague_Value_MIN)
        # 5 数值范围(最大值)
        self.pushButton_value_max.clicked.connect(self.Gague_Value_MAX)
        # 6 生成固件
        self.pushButton_build.clicked.connect(self.Gague_Build)

        # 初始化表盘背景图
        defaultPix1 = QtGui.QPixmap("./meter_images/gague_temp.png")
        self.label_gague.setPixmap(defaultPix1)

        # 初始化表盘指针svg
        defaultPix2 = QtGui.QPixmap("./meter_images/dx.svg")
        # 旋转pix
        self.rotation = -45
        self.transform = QtGui.QTransform().rotate(self.rotation)
        defaultPix2 = defaultPix2.transformed(self.transform, QtCore.Qt.SmoothTransformation)
        self.label_pointer.setPixmap(defaultPix2)

        # 初始化数值样式
        self.label_value.setStyleSheet('color:' + self.value_color + '; background: transparent;')

        # 显示界面
        self.show()


    # 1 表盘选择
    def Gague_Choose(self):
        # 表盘文件选择对话框
        # directory = QtWidgets.QFileDialog.getOpenFileName(self,
        #       "选择表盘文件","./",
        #       "All Files (*); PNG Files (*.png)") 

        FileName, FileType = QtWidgets.QFileDialog.getOpenFileName(self,
        "选择表盘文件", os.getcwd(),
        "PNG Files (*.png)") 

        if(len(FileName) != 0):

            # 刷新表盘背景图
            defaultPix1 = QtGui.QPixmap(FileName)
            
            # 暂存表盘背景图片
            # QtGui.QPixmap.drawPixmap(0,0,320,240,QtGui.QPixmap(FileName))
            defaultPix1.save("./meter_images/gague_temp.png")

            self.label_gague.setPixmap(defaultPix1)

        # print("------->")
        # print(FileName)
        # print("------->")
        # print(FileType)


    
    # 2 表盘指针颜色修改
    def Gague_Pointer_ColorChange(self):

        # 打开颜色识获器
        my_color_picker = ColorPicker(useAlpha=False)
        picker_color = my_color_picker.rgb2hex(my_color_picker.getColor())
        # print("------->")
        # print(picker_color)

        pointer_color = '#' + picker_color

        # 生成新的svg图形
        with  open('./meter_images/dx.svg','w',encoding = 'utf-8') as f:
            f.write('<svg id="图层_1" data-name="图层 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5.67 127.56"><defs><style>.cls-1,.cls-2{fill:'+ pointer_color + ';}.cls-2{stroke:#000;stroke-miterlimit:10;stroke-width:0.25px;}</style></defs><title>指针45</title><polygon class="cls-1" points="5.67 127.56 0 127.56 2.83 0 4.25 63.78 5.67 127.56"/><polygon class="cls-1" points="1.42 63.78 2.83 63.78 4.25 63.78 5.67 127.56 0 127.56 1.42 63.78"/><polygon class="cls-2" points="1.42 63.78 4.25 63.78 2.83 0 1.42 63.78"/></svg>')
            f.close()

        # 将表盘指针颜色写入Config json文件
        with open('./gaguge_config.json', 'r', encoding='utf8') as read_congfig_file:
            str_temp = read_congfig_file.read()
            json_data = json.loads(str_temp)
            self.value_color = json_data['value_color']
            self.value_min = json_data['value_min']
            self.value_max = json_data['value_max']
            value_min_str = str(self.value_min)
            value_max_str = str(self.value_max)
            json_data['pointer_color'] = pointer_color
            write_json =  json_data
        with  open('./gaguge_config.json','w+',encoding = 'utf-8') as congfig_file:
            json.dump(write_json, congfig_file, indent=4, sort_keys=True)


        # 生成新的home_page.xml文件
        with  open('./meter_images/home_page.xml','w',encoding = 'utf-8') as f:
            f.write('''<?xml ruler_y="220" ruler_x="297,42,-439,-112"?>
<window name="home_page" style:normal:bg_color="#FFFFFF">
<guage name="guage" x="0" y="0" w="320" h="240" draw_type="scale_auto" image="voltmeter">
    <guage_pointer name="guage_pointer" x="294" y="10" w="7" h="420" value="0" angle="-90" anchor_x="0.5" anchor_y="0.5" animation="value(easing=bounce_out,from=0,to=-90)" min="-90" max="0" style:normal:fg_color="#00000000" style:normal:bg_color="''' + pointer_color + '''" image="pointer_2" style:normal:border="all" style:normal:border_color="#00000000"/>
</guage>
<label name="val" x="221" y="155" w="89" h="75" style:normal:font_size="30" style:normal:text_color="'''+ self.value_color +'''" style:normal:text_align_h="right" visible="true" min="'''+ value_min_str + '''" max="'''+ value_max_str + '''" enable="true" style:normal:font_name="default" text="0"/>
</window>''')
            f.close()

        # 刷新表盘指针svg
        defaultPix2 = QtGui.QPixmap("./meter_images/dx.svg")
        # 旋转pix
        self.rotation = -45
        self.transform = QtGui.QTransform().rotate(self.rotation)
        defaultPix2 = defaultPix2.transformed(self.transform, QtCore.Qt.SmoothTransformation)
        self.label_pointer.setPixmap(defaultPix2)


    # 3 表盘数值颜色修改
    def Gague_Value_ColorChange(self):

        # 打开颜色识获器
        my_color_picker = ColorPicker(useAlpha=False)
        picker_color = my_color_picker.rgb2hex(my_color_picker.getColor())
        # print("------->")
        # print(picker_color)

        value_color = '#' + picker_color

        self.label_value.setStyleSheet('color:' + value_color + '; background: transparent;')

        # 将数值颜色写入Config json文件
        with open('./gaguge_config.json', 'r', encoding='utf8') as read_congfig_file:
            str_temp = read_congfig_file.read()
            json_data = json.loads(str_temp)
            self.pointer_color = json_data['pointer_color']
            self.value_min = json_data['value_min']
            self.value_max = json_data['value_max']
            value_min_str = str(self.value_min)
            value_max_str = str(self.value_max)
            json_data['value_color'] = value_color
            write_json =  json_data
        with  open('./gaguge_config.json','w+',encoding = 'utf-8') as congfig_file:
            json.dump(write_json, congfig_file, indent=4, sort_keys=True)

        # 生成新的home_page.xml文件
        with  open('./meter_images/home_page.xml','w',encoding = 'utf-8') as f:
            f.write('''<?xml ruler_y="220" ruler_x="297,42,-439,-112"?>
<window name="home_page" style:normal:bg_color="#FFFFFF">
<guage name="guage" x="0" y="0" w="320" h="240" draw_type="scale_auto" image="voltmeter">
    <guage_pointer name="guage_pointer" x="294" y="10" w="7" h="420" value="0" angle="-90" anchor_x="0.5" anchor_y="0.5" animation="value(easing=bounce_out,from=0,to=-90)" min="-90" max="0" style:normal:fg_color="#00000000" style:normal:bg_color="''' + self.pointer_color + '''" image="pointer_2" style:normal:border="all" style:normal:border_color="#00000000"/>
</guage>
<label name="val" x="221" y="155" w="89" h="75" style:normal:font_size="30" style:normal:text_color="'''+ self.value_color +'''" style:normal:text_align_h="right" visible="true" min="'''+ value_min_str + '''" max="'''+ value_max_str + '''" enable="true" style:normal:font_name="default" text="0"/>
</window>''')
            f.close()


    # 4 表盘数值(最小值)修改
    def Gague_Value_MIN(self):
        
        # 第一个参数为父组件；
        # 第二个参数为对话框标题；
        # 第三个参数为对话框提示信息；
        # 第四个参数为默认值；
        # 第五个参数为允许输入的最小值；
        # 第六个参数为允许输入的最大值；
        # 第七个参数为步长
        # num, ok = QInputDialog.getInt(self,'获取整数','输入您的数字(-10～10)',0,-10,10,1)
        num_min, ok  = QInputDialog.getInt(self, "表盘最小值修改", "输入最小值",0,0)
        if(ok):
            print(num_min)
            # 将最小值写入Config json文件
            with open('./gaguge_config.json', 'r', encoding='utf8') as read_congfig_file:
                str_temp = read_congfig_file.read()
                json_data = json.loads(str_temp)
                self.pointer_color = json_data['pointer_color']
                self.value_color = json_data['value_color']
                self.value_max = json_data['value_max']
                json_data['value_min'] = num_min
                write_json =  json_data
            with  open('./gaguge_config.json','w+',encoding = 'utf-8') as congfig_file:
                json.dump(write_json, congfig_file, indent=4, sort_keys=True)

            self.value_num_min = num_min

            value_min_str = str(self.value_num_min)
            value_max_str = str(self.value_max)

            # 生成新的home_page.xml文件
            with  open('./meter_images/home_page.xml','w',encoding = 'utf-8') as f:
                f.write('''<?xml ruler_y="220" ruler_x="297,42,-439,-112"?>
    <window name="home_page" style:normal:bg_color="#FFFFFF">
    <guage name="guage" x="0" y="0" w="320" h="240" draw_type="scale_auto" image="voltmeter">
        <guage_pointer name="guage_pointer" x="294" y="10" w="7" h="420" value="0" angle="-90" anchor_x="0.5" anchor_y="0.5" animation="value(easing=bounce_out,from=0,to=-90)" min="-90" max="0" style:normal:fg_color="#00000000" style:normal:bg_color="''' + self.pointer_color + '''" image="pointer_2" style:normal:border="all" style:normal:border_color="#00000000"/>
    </guage>
    <label name="val" x="221" y="155" w="89" h="75" style:normal:font_size="30" style:normal:text_color="'''+ self.value_color +'''" style:normal:text_align_h="right" visible="true" min="'''+ value_min_str + '''" max="'''+ value_max_str + '''" enable="true" style:normal:font_name="default" text="0"/>
    </window>''')
                f.close()

        
    # 5 表盘数值(最大值)修改
    def Gague_Value_MAX(self):
        num_max, ok  = QInputDialog.getInt(self, "表盘最大值修改", "输入最大值")
        if(ok):
            print(num_max)
            # 将最大值写入Config json文件
            with open('./gaguge_config.json', 'r', encoding='utf8') as read_congfig_file:
                str_temp = read_congfig_file.read()
                json_data = json.loads(str_temp)
                self.pointer_color = json_data['pointer_color']
                self.value_color = json_data['value_color']
                self.value_min = json_data['value_min']
                json_data['value_max'] = num_max
                write_json =  json_data
            with  open('./gaguge_config.json','w+',encoding = 'utf-8') as congfig_file:
                json.dump(write_json, congfig_file, indent=4, sort_keys=True)

            self.value_num_max = num_max

            value_min_str = str(self.value_min)
            value_max_str = str(self.value_num_max)

            # 生成新的home_page.xml文件
            with  open('./meter_images/home_page.xml','w',encoding = 'utf-8') as f:
                f.write('''<?xml ruler_y="220" ruler_x="297,42,-439,-112"?>
    <window name="home_page" style:normal:bg_color="#FFFFFF">
    <guage name="guage" x="0" y="0" w="320" h="240" draw_type="scale_auto" image="voltmeter">
        <guage_pointer name="guage_pointer" x="294" y="10" w="7" h="420" value="0" angle="-90" anchor_x="0.5" anchor_y="0.5" animation="value(easing=bounce_out,from=0,to=-90)" min="-90" max="0" style:normal:fg_color="#00000000" style:normal:bg_color="''' + self.pointer_color + '''" image="pointer_2" style:normal:border="all" style:normal:border_color="#00000000"/>
    </guage>
    <label name="val" x="221" y="155" w="89" h="75" style:normal:font_size="30" style:normal:text_color="'''+ self.value_color +'''" style:normal:text_align_h="right" visible="true" min="'''+ value_min_str + '''" max="'''+ value_max_str + '''" enable="true" style:normal:font_name="default" text="0"/>
    </window>''')
                f.close()

    # 6 生成固件
    def Gague_Build(self):

        # 删除文件
        self.Del_FireWareFile("./meter_file/48_PAN/gauge_320_240_90/design/default/images/svg/pointer.bsvg")
        self.Del_FireWareFile("./meter_file/48_PAN/gauge_320_240_90/design/default/images/svg/pointer_1.bsvg")
        self.Del_FireWareFile("./meter_file/48_PAN/gauge_320_240_90/design/default/images/svg/pointer_2.bsvg")
        self.Del_FireWareFile("./meter_file/48_PAN/gauge_320_240_90/design/default/ui/home_page.bin")
        self.Del_FireWareFile("./meter_file/48_PAN/gauge_320_240_90/design/default/ui/new.bin")
        self.Del_FireWareFile("./meter_file/48_PAN/gauge_320_240_90/design/default/images/xx/voltmeter.png")
        self.Del_FireWareFile("./meter_file/48_PAN/gauge_320_240_90/assets.HJR")

        # 复制文件 xml
        self.Copy_FireWareFile(r".\meter_images\home_page.xml", r"meter_file\48_PAN\gauge_320_240_90\design\default\ui\home_page.xml")

        # 生成svg图片bin
        subprocess.run(r".\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\bsvggen.exe .\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer.svg .\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer.bsvg bin")
        subprocess.run(r".\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\bsvggen.exe .\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer_1.svg .\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer_1.bsvg bin")
        subprocess.run(r".\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\bsvggen.exe .\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer_2.svg .\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer_2.bsvg bin")
        # 生成ui xml文件bin
        subprocess.run(r".\meter_file\48_PAN\gauge_320_240_90\design\default\ui\xml_to_ui.exe .\meter_file\48_PAN\gauge_320_240_90\design\default\ui\home_page.xml .\meter_file\48_PAN\gauge_320_240_90\design\default\ui\home_page.bin bin")
        subprocess.run(r".\meter_file\48_PAN\gauge_320_240_90\design\default\ui\xml_to_ui.exe .\meter_file\48_PAN\gauge_320_240_90\design\default\ui\new.xml .\meter_file\48_PAN\gauge_320_240_90\design\default\ui\new.bin bin")        
        
        # 复制文件 
        self.Copy_FireWareFile(r".\meter_images\gague_temp.png", r".\meter_file\48_PAN\gauge_320_240_90\design\default\images\xx\voltmeter.png")
        self.Copy_FireWareFile(r".\meter_images\gague_temp.png", r".\meter_file\48_PAN\gauge_320_240_90\res\assets\default\raw\images\xx\voltmeter.png")

        self.Copy_FireWareFile(r".\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer.bsvg", r".\meter_file\48_PAN\gauge_320_240_90\res\assets\default\raw\images\svg\pointer.bsvg")
        self.Copy_FireWareFile(r".\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer_1.bsvg", r".\meter_file\48_PAN\gauge_320_240_90\res\assets\default\raw\images\svg\pointer_1.bsvg")
        self.Copy_FireWareFile(r".\meter_file\48_PAN\gauge_320_240_90\design\default\images\svg\pointer_2.bsvg", r".\meter_file\48_PAN\gauge_320_240_90\res\assets\default\raw\images\svg\pointer_2.bsvg")

        self.Copy_FireWareFile(r".\meter_file\48_PAN\gauge_320_240_90\design\default\ui\new.bin", r".\meter_file\48_PAN\gauge_320_240_90\res\assets\default\raw\ui\new.bin")
        self.Copy_FireWareFile(r".\meter_file\48_PAN\gauge_320_240_90\design\default\ui\home_page.bin", r".\meter_file\48_PAN\gauge_320_240_90\res\assets\default\raw\ui\home_page.bin")

        # # 生成最终固件
        subprocess.run(r".\meter_file\48_PAN\gauge_320_240_90\.\genromfs.exe -d .\meter_file\48_PAN\gauge_320_240_90\res -f .\meter_fireware\assets.HJR")
        QMessageBox.about(self, "固件生成信息", "表盘固件生成成功!")


    # 删除文件
    def Del_FireWareFile(self, filename):
        file_flag = os.path.exists(filename)
        if(file_flag == True):
            # print("---->del")
            os.remove(filename)

    # 复制文件
    def Copy_FireWareFile(self, src_filename, des_filename):
        shutil.copyfile(src_filename, des_filename)


    # 主程序全局关闭事件监听
    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    # QSystemTrayIcon.NoIcon
    # QSystemTrayIcon.Information
    # QSystemTrayIcon.Warning
    # QSystemTrayIcon.Critical
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.dx_SystemTray1.showMsg(1, "程序缩小至系统托盘!")


    # 系统托盘类信号数据处理
    def SystemTray_Pro(self,str_info):
        if(str_info == "show"):
            self.showApp_dx()
        elif(str_info == "close"):
            self.closeApp_dx()


    # 关闭程序
    def closeApp_dx(self):
        # 点击关闭按钮或者点击退出事件会出现图标无法消失的bug，需要手动将图标内存清除
        sys.exit(app.exec_())

    # 显示程序
    def showApp_dx(self):
        self.show()

# 主函数-------------------------------------
if __name__ == '__main__':

    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)

    app.setApplicationName("智能表盘生成器V1.0")

    # 设置成Fusion样式
    app.setStyle("Fusion")
    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet(
        "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
    )

    # setup stylesheet
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # qtmodern.styles.dark(app)

    main_win = mainWin()
    main_win.setWindowTitle('智能表盘生成器V1.0')
    #禁止最大化按钮
    main_win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
    #禁止拉伸窗口大小
    main_win.setFixedSize(main_win.width(), main_win.height());  
    main_win.show()

    sys.exit(app.exec_())