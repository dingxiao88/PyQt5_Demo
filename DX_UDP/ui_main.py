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
        MainWindow.resize(696, 434)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_UDP = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_UDP.setGeometry(QtCore.QRect(50, 30, 571, 141))
        self.groupBox_UDP.setFlat(False)
        self.groupBox_UDP.setCheckable(False)
        self.groupBox_UDP.setObjectName("groupBox_UDP")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_UDP)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 188, 22))
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
        self.pushButton_udpSend.setGeometry(QtCore.QRect(477, 90, 75, 23))
        self.pushButton_udpSend.setObjectName("pushButton_udpSend")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_UDP)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 90, 188, 22))
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
        self.layoutWidget_3.setGeometry(QtCore.QRect(257, 90, 188, 22))
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
        self.layoutWidget1.setGeometry(QtCore.QRect(257, 30, 188, 22))
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
        self.pushButton_bing.setGeometry(QtCore.QRect(477, 30, 75, 23))
        self.pushButton_bing.setObjectName("pushButton_bing")
        self.groupBox_Weather = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Weather.setGeometry(QtCore.QRect(50, 190, 571, 181))
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
        self.pushButton_City_Check = QtWidgets.QPushButton(self.groupBox_Weather)
        self.pushButton_City_Check.setGeometry(QtCore.QRect(460, 70, 75, 23))
        self.pushButton_City_Check.setObjectName("pushButton_City_Check")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_UDP.setTitle(_translate("MainWindow", "UDP测试"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">本地IP:</span></p></body></html>"))
        self.lineEdit_Local_IP.setPlaceholderText(_translate("MainWindow", "192.168.41.4"))
        self.pushButton_udpSend.setText(_translate("MainWindow", "发送"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">远端IP:</span></p></body></html>"))
        self.lineEdit_Remote_IP.setPlaceholderText(_translate("MainWindow", "192.168.41.6"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">远端Port:</span></p></body></html>"))
        self.lineEdit_Remote_Port.setPlaceholderText(_translate("MainWindow", "8881"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">本地Port:</span></p></body></html>"))
        self.lineEdit_Local_Port.setPlaceholderText(_translate("MainWindow", "8883"))
        self.pushButton_bing.setText(_translate("MainWindow", "绑定"))
        self.groupBox_Weather.setTitle(_translate("MainWindow", "天气查询"))
        self.pushButton_Weather_Check.setText(_translate("MainWindow", "查询"))
        self.label_3.setText(_translate("MainWindow", "查询城市"))
        self.pushButton_City_Check.setText(_translate("MainWindow", "城市查询"))
