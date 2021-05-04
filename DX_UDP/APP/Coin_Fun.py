
from Thread_GetPrice import DX_Thread_GetPrice


# url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=eur%2Cgbp%2Cusd&include_24hr_change=true"
# url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC"
# url =  'http://wthrcdn.etouch.cn/weather_mini?citykey=101010100'

url_base = 'https://api.coingecko.com/api/v3/simple/price?ids='
url_last = '&vs_currencies=eur%2Cgbp%2Cusd&include_24hr_change=true'



# 获得单一数字货币实时价格
def GetSingleCoinRealPrice(self):

    self.pushButton_getRealPrice.setEnabled(False)
    self.pushButton_getRealPrice.setText('获取中...')

    self.label_coinRealPrice.setText('checking...')

    coinName = self.lineEdit_coinName.text()
    if not coinName:
        coinName = 'bitcoin'
    
    GetPriceThread(self,coinName, 0, 0)


# 获得多个数字货币实时价格
def GetMultiCoinRealPrice(self, list_index, first_clean):
    
    self.pushButton_getRealPrice_2.setEnabled(False)
    self.pushButton_getRealPrice_2.setText('获取中...')

    if(first_clean == 1):
        self.label_showPrice1.setText(' ')
        self.label_showPrice2.setText(' ')
        self.label_showPrice3.setText(' ')
        self.label_showPrice4.setText(' ')

    GetPriceThread(self, self.coinList[list_index], 1, list_index)

# 获得实时价格线程
def GetPriceThread(self, coinName, ThreadMode, list_index):
    # 线程启动按钮绑定事件------------
    self.dx_getPrice = DX_Thread_GetPrice("dx_getPrice", coinName, ThreadMode, list_index)
    self.dx_getPrice.DX_Thread_OutSingal.connect(self.ShowMoney)
    self.dx_getPrice.setRun(True)
    self.dx_getPrice.start()


# 计算盈亏比
def GetMoney(self):

    price = float(self.lineEdit_coinPrice.text())

    price_1 = price + (price * 0.01)
    price_1_23 = price + (price * 0.0123)
    price_2_23 = price + (price * 0.0223)
    price_3 = price + (price * 0.03)
    price_5 = price + (price * 0.05)
    price_8 = price + (price * 0.08)
    price_10 = price + (price * 0.10)
    price_20 = price + (price * 0.20)

    price_1_f = price - (price * 0.01)
    price_2_f = price - (price * 0.02)
    price_3_f = price - (price * 0.03)
    price_4_f = price - (price * 0.04)
    price_5_f = price - (price * 0.05)
    price_6_f = price - (price * 0.06)
    price_7_f = price - (price * 0.07)
    price_8_f = price - (price * 0.08)

    self.label_moneyGetGood.setText(
    'each good price is \n' +
    '1% = ' + str(price_1) + '\n' +
    '1.23% = ' + str(price_1_23) + '\n' +
    '2.23% = ' + str(price_2_23) + '\n' +
    '3% = ' + str(price_3) + '\n' +
    '5% = ' + str(price_5) + '\n' +
    '8% = ' + str(price_8) + '\n' +
    '10% = ' + str(price_10) + '\n' +
    '20% = ' + str(price_20) + '\n' 
    )

    self.label_moneyGetBad.setText(
    'each bad price is \n' +
    '1% = ' + str(price_1_f) + '\n' +
    '2% = ' + str(price_2_f) + '\n' +
    '3% = ' + str(price_3_f) + '\n' +
    '4% = ' + str(price_4_f) + '\n' +
    '5% = ' + str(price_5_f) + '\n' +
    '6% = ' + str(price_6_f) + '\n' +
    '7% = ' + str(price_7_f) + '\n' +
    '8% = ' + str(price_8_f) + '\n' 
    )