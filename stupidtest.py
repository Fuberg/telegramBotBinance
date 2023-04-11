import telebot
from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from time import time, sleep
from rsi import *
from SMA import *
from EMA import *
from MACD import *

bot = telebot.TeleBot('5682781667:AAEa5N2CQZj72HzSf0UDnf_MedKMTMn6IP8')

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    
    # Здесь будет храниться итоговый текствоый результат работы, который мы отправим пользователю 
    text_result = "М30 \n"
    
    # init
    api_key = 'iT5OQUSTU8NIUYHYb44mXZlyOWtozSbr0eXGHCdyvksl1aRRi5z7rPEsGC99aTTs'
    api_secret = 'bzHH1jgTwfhaBrwrUvUBvtznUWYoqnmnfGoCUlT8GdsxcMzNkt0FpvIV2BMTPmUB'

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
                                                             startTime=None, endTime=None, limit=20)
        
        for candle in ticker_candles:
            tickers_data[ticker]["O"].append(float(candle.open))
            tickers_data[ticker]["H"].append(float(candle.high))
            tickers_data[ticker]["L"].append(float(candle.low))
            tickers_data[ticker]["C"].append(float(candle.close))
            tickers_data[ticker]["V"].append(int(float(candle.volume)))
        if ticker == "BTCUSDT":
            bot.send_message(message.chat.id, str(tickers_data[ticker]["C"]))
        
        # Удаляем последние элементы массивов, потому что эта свеча еще не сформировалась
        
bot.polling(none_stop=True, interval=0)