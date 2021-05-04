
#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time

import urllib.request
import json


# url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=eur%2Cgbp%2Cusd&include_24hr_change=true"
# url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC"
# url =  'http://wthrcdn.etouch.cn/weather_mini?citykey=101010100'

url_base = 'https://api.coingecko.com/api/v3/simple/price?ids='
url_last = '&vs_currencies=eur%2Cgbp%2Cusd&include_24hr_change=true'

class DX_Thread_GetPrice(QThread):

    DX_Thread_OutSingal = pyqtSignal(str, int, int)

    def __init__(self, name, coin_name, mode, index, parent = None):
        super(DX_Thread_GetPrice, self).__init__(parent)
        self.name = name
        self.coinName = coin_name
        self.working_flag = False
        self.working_mode = mode
        self.index = index
        # print(self.name)


    # 线程运行控制
    def setRun(self, run_status):
        if(run_status == False):
            self.working_flag = False
            # self.DX_Thread_OutSingal.emit('thread set run', 1)

        elif(run_status == True):
            self.working_flag = True
            # self.DX_Thread_OutSingal.emit('thread set stop', 0)

    def getRunStatus(self):
        return self.working_flag


    # 线程运行主循环
    def run(self):
        if(self.working_flag == True):
            url = url_base + self.coinName + url_last

            # print(url)

            response = urllib.request.urlopen(url)
            the_page = response.read()
            data = json.loads(the_page)

            try:
                temp_value = data[self.coinName]['usd']
                # temp_value = data[coinName]['eur']
                # temp_value = data[coinName]['gbp']
            except:
                temp_value = 'This Coin is not available'

            temp_price = str(temp_value)

            # print(temp_value)

            if(self.working_mode == 0):
                self.DX_Thread_OutSingal.emit(self.coinName + ' RealPrice: $ ' + temp_price, self.working_mode, self.index)
            elif(self.working_mode == 1):
                self.DX_Thread_OutSingal.emit(self.coinName + '\n$ ' + temp_price, self.working_mode, self.index)
            # self.label_coinRealPrice.setText(coinName + ' RealPrice: $' + temp_price)
            # self.DX_Thread_OutSingal.emit(temp_price)
        