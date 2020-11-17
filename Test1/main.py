# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
# ui_test.py中内容
from ui_test import *

# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)  
        self.setupUi(self)
        # 将响应函数绑定到指定Button
        self.pushButton.clicked.connect(self.showMessage1)
        self.pushButton_2.clicked.connect(self.showMessage2)

    # Button响应函数
    def showMessage1(self):
        self.textEdit.setText('hello world')
    # Button响应函数
    def showMessage2(self):
        self.textEdit.setText('dingxiao')

if __name__ == '__main__':
    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.show()
    sys.exit(app.exec_())