# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1033, 509)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_UDP = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_UDP.setGeometry(QtCore.QRect(20, 20, 571, 141))
        self.groupBox_UDP.setFlat(False)
        self.groupBox_UDP.setCheckable(False)
        self.groupBox_UDP.setObjectName("groupBox_UDP")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_UDP)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 188, 22))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_Local_IP = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_Local_IP.setObjectName("lineEdit_Local_IP")
        self.horizontalLayout.addWidget(self.lineEdit_Local_IP)
        self.pushButton_udpSend = QtWidgets.QPushButton(self.groupBox_UDP)
        self.pushButton_udpSend.setGeometry(QtCore.QRect(470, 80, 75, 23))
        self.pushButton_udpSend.setObjectName("pushButton_udpSend")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_UDP)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 50, 188, 22))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_Remote_IP = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.lineEdit_Remote_IP.setText("")
        self.lineEdit_Remote_IP.setObjectName("lineEdit_Remote_IP")
        self.horizontalLayout_4.addWidget(self.lineEdit_Remote_IP)
        self.layoutWidget_3 = QtWidgets.QWidget(self.groupBox_UDP)
        self.layoutWidget_3.setGeometry(QtCore.QRect(260, 50, 188, 22))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.lineEdit_Remote_Port = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_Remote_Port.setObjectName("lineEdit_Remote_Port")
        self.horizontalLayout_5.addWidget(self.lineEdit_Remote_Port)
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_UDP)
        self.layoutWidget1.setGeometry(QtCore.QRect(260, 20, 188, 22))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_Local_Port = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_Local_Port.setObjectName("lineEdit_Local_Port")
        self.horizontalLayout_2.addWidget(self.lineEdit_Local_Port)
        self.pushButton_bing = QtWidgets.QPushButton(self.groupBox_UDP)
        self.pushButton_bing.setGeometry(QtCore.QRect(470, 40, 75, 23))
        self.pushButton_bing.setObjectName("pushButton_bing")
        self.textEdit_udpSendData = QtWidgets.QTextEdit(self.groupBox_UDP)
        self.textEdit_udpSendData.setGeometry(QtCore.QRect(30, 80, 421, 51))
        self.textEdit_udpSendData.setObjectName("textEdit_udpSendData")
        self.pushButton_udpSend_continue = QtWidgets.QPushButton(self.groupBox_UDP)
        self.pushButton_udpSend_continue.setGeometry(QtCore.QRect(470, 110, 75, 23))
        self.pushButton_udpSend_continue.setObjectName("pushButton_udpSend_continue")
        self.groupBox_Weather = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Weather.setGeometry(QtCore.QRect(20, 180, 571, 181))
        self.groupBox_Weather.setObjectName("groupBox_Weather")
        self.textEdit_Weather = QtWidgets.QTextEdit(self.groupBox_Weather)
        self.textEdit_Weather.setGeometry(QtCore.QRect(20, 20, 401, 141))
        self.textEdit_Weather.setObjectName("textEdit_Weather")
        self.pushButton_Weather_Check = QtWidgets.QPushButton(self.groupBox_Weather)
        self.pushButton_Weather_Check.setGeometry(QtCore.QRect(460, 140, 75, 23))
        self.pushButton_Weather_Check.setObjectName("pushButton_Weather_Check")
        self.lineEdit_Weather_City = QtWidgets.QLineEdit(self.groupBox_Weather)
        self.lineEdit_Weather_City.setGeometry(QtCore.QRect(440, 40, 113, 20))
        self.lineEdit_Weather_City.setObjectName("lineEdit_Weather_City")
        self.label_3 = QtWidgets.QLabel(self.groupBox_Weather)
        self.label_3.setGeometry(QtCore.QRect(470, 20, 54, 12))
        self.label_3.setObjectName("label_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 370, 571, 80))
        self.groupBox.setObjectName("groupBox")
        self.textEdit_thread = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_thread.setGeometry(QtCore.QRect(20, 20, 401, 51))
        self.textEdit_thread.setObjectName("textEdit_thread")
        self.pushButton_thread_clean = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_thread_clean.setGeometry(QtCore.QRect(460, 50, 75, 23))
        self.pushButton_thread_clean.setObjectName("pushButton_thread_clean")
        self.pushButton_thread_start = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_thread_start.setGeometry(QtCore.QRect(460, 20, 75, 23))
        self.pushButton_thread_start.setObjectName("pushButton_thread_start")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(610, 20, 401, 431))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 70, 181, 61))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_6.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Pixel LCD7")
        font.setPointSize(26)
        self.label_6.setFont(font)
        self.label_6.setAutoFillBackground(False)
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(210, 70, 181, 61))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_7.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Pixel LCD7")
        font.setPointSize(26)
        self.label_7.setFont(font)
        self.label_7.setAutoFillBackground(False)
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(70, 40, 47, 20))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(280, 40, 47, 20))
        self.label_9.setObjectName("label_9")
        self.line = QtWidgets.QFrame(self.groupBox_2)
        self.line.setGeometry(QtCore.QRect(10, 200, 381, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 230, 161, 171))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_DC_FYRunCtl = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_DC_FYRunCtl.setGeometry(QtCore.QRect(40, 30, 81, 51))
        self.pushButton_DC_FYRunCtl.setObjectName("pushButton_DC_FYRunCtl")
        self.pushButton_DC_FYRun_Up = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_DC_FYRun_Up.setGeometry(QtCore.QRect(20, 100, 51, 51))
        self.pushButton_DC_FYRun_Up.setObjectName("pushButton_DC_FYRun_Up")
        self.pushButton_DC_FYRun_Down = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_DC_FYRun_Down.setGeometry(QtCore.QRect(90, 100, 51, 51))
        self.pushButton_DC_FYRun_Down.setObjectName("pushButton_DC_FYRun_Down")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(220, 230, 161, 171))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton_DC_XHRunCtl = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_DC_XHRunCtl.setGeometry(QtCore.QRect(40, 30, 81, 51))
        self.pushButton_DC_XHRunCtl.setObjectName("pushButton_DC_XHRunCtl")
        self.pushButton_DC_XHRun_Left = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_DC_XHRun_Left.setGeometry(QtCore.QRect(20, 100, 51, 51))
        self.pushButton_DC_XHRun_Left.setObjectName("pushButton_DC_XHRun_Left")
        self.pushButton_DC_XHRun_Right = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_DC_XHRun_Right.setGeometry(QtCore.QRect(90, 100, 51, 51))
        self.pushButton_DC_XHRun_Right.setObjectName("pushButton_DC_XHRun_Right")
        self.label_DC_FYStatus = QtWidgets.QLabel(self.groupBox_2)
        self.label_DC_FYStatus.setGeometry(QtCore.QRect(150, 140, 41, 21))
        self.label_DC_FYStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.label_DC_FYStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DC_FYStatus.setObjectName("label_DC_FYStatus")
        self.label_DC_XHStatus = QtWidgets.QLabel(self.groupBox_2)
        self.label_DC_XHStatus.setGeometry(QtCore.QRect(350, 140, 41, 21))
        self.label_DC_XHStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.label_DC_XHStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DC_XHStatus.setObjectName("label_DC_XHStatus")
        self.label_udp_recv_count = QtWidgets.QLabel(self.groupBox_2)
        self.label_udp_recv_count.setGeometry(QtCore.QRect(10, 170, 381, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_udp_recv_count.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Pixel LCD7")
        font.setPointSize(18)
        self.label_udp_recv_count.setFont(font)
        self.label_udp_recv_count.setAutoFillBackground(False)
        self.label_udp_recv_count.setFrameShape(QtWidgets.QFrame.Box)
        self.label_udp_recv_count.setAlignment(QtCore.Qt.AlignCenter)
        self.label_udp_recv_count.setObjectName("label_udp_recv_count")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1033, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_thread_clean.clicked.connect(self.textEdit_thread.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DX测试"))
        self.groupBox_UDP.setTitle(_translate("MainWindow", "UDP测试"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">本地IP:</span></p></body></html>"))
        self.lineEdit_Local_IP.setPlaceholderText(_translate("MainWindow", "192.168.41.4"))
        self.pushButton_udpSend.setText(_translate("MainWindow", "发送"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">远端IP:</span></p></body></html>"))
        self.lineEdit_Remote_IP.setPlaceholderText(_translate("MainWindow", "224.100.23.200"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">远端Port:</span></p></body></html>"))
        self.lineEdit_Remote_Port.setPlaceholderText(_translate("MainWindow", "6000"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">本地Port:</span></p></body></html>"))
        self.lineEdit_Local_Port.setPlaceholderText(_translate("MainWindow", "6000"))
        self.pushButton_bing.setText(_translate("MainWindow", "绑定"))
        self.pushButton_udpSend_continue.setText(_translate("MainWindow", "连续发送"))
        self.groupBox_Weather.setTitle(_translate("MainWindow", "天气查询"))
        self.pushButton_Weather_Check.setText(_translate("MainWindow", "查询"))
        self.lineEdit_Weather_City.setPlaceholderText(_translate("MainWindow", "杭州"))
        self.label_3.setText(_translate("MainWindow", "查询城市"))
        self.groupBox.setTitle(_translate("MainWindow", "Thread"))
        self.pushButton_thread_clean.setText(_translate("MainWindow", "清空"))
        self.pushButton_thread_start.setText(_translate("MainWindow", "启动"))
        self.groupBox_2.setTitle(_translate("MainWindow", "装置信息"))
        self.label_6.setText(_translate("MainWindow", "0.00"))
        self.label_7.setText(_translate("MainWindow", "0.00"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">俯仰</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">旋回</span></p></body></html>"))
        self.groupBox_3.setTitle(_translate("MainWindow", "俯仰控制"))
        self.pushButton_DC_FYRunCtl.setText(_translate("MainWindow", "启动"))
        self.pushButton_DC_FYRun_Up.setText(_translate("MainWindow", "上"))
        self.pushButton_DC_FYRun_Down.setText(_translate("MainWindow", "下"))
        self.groupBox_4.setTitle(_translate("MainWindow", "旋回控制"))
        self.pushButton_DC_XHRunCtl.setText(_translate("MainWindow", "启动"))
        self.pushButton_DC_XHRun_Left.setText(_translate("MainWindow", "左"))
        self.pushButton_DC_XHRun_Right.setText(_translate("MainWindow", "右"))
        self.label_DC_FYStatus.setText(_translate("MainWindow", "未知"))
        self.label_DC_XHStatus.setText(_translate("MainWindow", "未知"))
        self.label_udp_recv_count.setText(_translate("MainWindow", "0"))
