from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from time import time, sleep
from rsi import *
# from MACD import *
# from Fractals import *
from SMA import *
from EMA import *
# from ATR import *
# from Confirmation import *


# init
api_key = '62v0KYZAwjt49c5y9NjYy8utDa0WaVJIH1aFf2cQTY8KWF60efr1ePvQXzKOdrUK'
api_secret = 'j5k8spQjWlFgXxEkKxgQnPxFQz29W7ZEmdTKVtdghXgzJg3vw2GHw1epYqUuMx8g'

# Через request_client мы будем взаимодействовать с API
request_client = RequestClient(api_key=api_key, secret_key=api_secret)

# Получаем все фьючерсы и их тикеры
all_futures_tickers = request_client.get_symbol_price_ticker()

# В этом массиве будут хранится тикеры (валютные пары), с которыми мы работаем
my_tickers = []

for futures in all_futures_tickers:
    if futures.symbol[-4:] == 'USDT':
        my_tickers.append(futures.symbol)

# В этом словаре будут хранится данные свечей для каждой валютной пары
tickers_data = dict()

# Эта переменная будет хранить значение времени последнего открытия
last_open_time = 0

# Получаем все данные и рассчитываем индикаторы
for ticker in my_tickers:
    tickers_data[ticker] = {"O": [], "H": [], "L": [], "C": [
    ], "V": [], "profit": [], "profit_direction": []}
    ticker_candles = request_client.get_candlestick_data(symbol=ticker, interval=CandlestickInterval.MIN30,
                                                         startTime=None, endTime=None, limit=15)
    for candle in ticker_candles:
        tickers_data[ticker]["O"].append(float(candle.open))
        tickers_data[ticker]["H"].append(float(candle.high))
        tickers_data[ticker]["L"].append(float(candle.low))
        tickers_data[ticker]["C"].append(float(candle.close))
        tickers_data[ticker]["V"].append(int(float(candle.volume)))
    # Удаляем последние элементы массивов, потому что эта свеча еще не сформировалась
    tickers_data[ticker]["O"].pop()
    tickers_data[ticker]["H"].pop()
    tickers_data[ticker]["L"].pop()
    tickers_data[ticker]["C"].pop()
    tickers_data[ticker]["V"].pop()
    
    if ticker == "BTCUSDT":
        print(tickers_data[ticker]["C"])

    # tickers_data[ticker]["RSI"] = RSI(tickers_data[ticker]["C"], periods=14)