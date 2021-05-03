import urllib.request
import json




# url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=eur%2Cgbp%2Cusd&include_24hr_change=true"
# url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC"
# url =  'http://wthrcdn.etouch.cn/weather_mini?citykey=101010100'

url_base = 'https://api.coingecko.com/api/v3/simple/price?ids='
url_last = '&vs_currencies=eur%2Cgbp%2Cusd&include_24hr_change=true'


def GetCoinRealPrice(self):

    self.label_coinRealPrice.setText('checking...')

    coinName = self.lineEdit_coinName.text()
    if not coinName:
        coinName = 'bitcoin'
    

    url = url_base + coinName + url_last

    # print(url)

    response = urllib.request.urlopen(url)
    the_page = response.read()
    data = json.loads(the_page)

    try:
        temp_value = data[coinName]['usd']
        # temp_value = data[coinName]['eur']
        # temp_value = data[coinName]['gbp']
    except:
        temp_value = 'This Coin is not available'

    temp_price = str(temp_value)

    # print(temp_value)
    self.label_coinRealPrice.setText(coinName + ' RealPrice: $' + temp_price)



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