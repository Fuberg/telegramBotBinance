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
                                                             startTime=None, endTime=None, limit=1000)
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

        tickers_data[ticker]["RSI"] = RSI(tickers_data[ticker]["C"], periods=14)

        # Получаем значения MACD, ее цвета и скользящие средние, используемые для расчета
        tickers_data[ticker]["MACD"], tickers_data[ticker]["MACD_Color"], tickers_data[ticker]["EMA12"], tickers_data[ticker]["EMA26"], tickers_data[ticker]["Signal"] = getMACD(tickers_data[ticker]["C"], 12, 26, 9)
        
        last_open_time = ticker_candles[len(ticker_candles)-2].openTime
        
        if ticker == "ARPAUSDT":
            bot.send_message(message.chat.id, str(tickers_data[ticker]["C"][len(tickers_data[ticker]["C"])-1]))
        

    for ticker in my_tickers[:]:
        if (len(tickers_data[ticker]["C"]) < 999):
            del tickers_data[ticker]
            my_tickers.remove(ticker)
    
    text_result = "M30 \n"
    
    for ticker in my_tickers:
        if ticker == "ARPAUSDT":
            bot.send_message(message.chat.id, str(tickers_data[ticker]["C"][len(tickers_data[ticker]["C"])-1]))
        
        macd_hist_3 = tickers_data[ticker]["MACD"][len(tickers_data[ticker]["C"])-3] - tickers_data[ticker]["Signal"][len(tickers_data[ticker]["C"])-3]
        macd_hist_2 = tickers_data[ticker]["MACD"][len(tickers_data[ticker]["C"])-2] - tickers_data[ticker]["Signal"][len(tickers_data[ticker]["C"])-2]
        macd_hist_1 = tickers_data[ticker]["MACD"][len(tickers_data[ticker]["C"])-1] - tickers_data[ticker]["Signal"][len(tickers_data[ticker]["C"])-1]
        # bot.send_message(message.chat.id, str(ticker) + " = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]))
        if ((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2] > 65) and (((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1] < tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2]) and (tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-3] < tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2])) or ((macd_hist_1 > 0) and (macd_hist_1 < macd_hist_2) and (macd_hist_3 < macd_hist_2)))):
            if len(text_result) < 3700:
                text_result += str(ticker) + " - ↧" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | " + '\n'
            else:
                bot.send_message(message.chat.id, text_result)
                text_result = ""
                text_result += str(ticker) + " - ↧" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | " + '\n'
            # text_result += str(ticker) + " - ↧" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | " + '\n'
        elif ((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2] < 35) and (((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1] > tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2]) and (tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-3] > tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2])) or ((macd_hist_1 < 0) and (macd_hist_1 > macd_hist_2) and (macd_hist_2 < macd_hist_3)))):
            if len(text_result) < 3700:
                text_result += str(ticker) + " - ↥" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | "  + '\n'
            else:
                bot.send_message(message.chat.id, text_result)
                text_result = ""
                text_result += str(ticker) + " - ↥" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | "  + '\n'
    
    if text_result != "":
        bot.send_message(message.chat.id, text_result)
    
    while True:
        # while True:
        #     try:
        #         time_test_candle = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN30,
        #                                                    startTime=None, endTime=None, limit=2)
        #         break
        #     except:
        #         sleep(10)
        #         continue
        time_test_candle = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN30,
                                                           startTime=None, endTime=None, limit=2)
        
        if (time_test_candle[0].openTime == last_open_time):
            sleep(15)
            continue
        else:
            last_open_time = time_test_candle[0].openTime
            # Началась новая свеча
            # TODO : Проверяем, есть ли у нас открытые позиции, если да, то закрываем их
            for ticker in my_tickers:
                # Получаем значения последних двух свечей
                # while True:
                #     try:
                #         ticker_candles = request_client.get_candlestick_data(
                #             symbol=ticker, interval=CandlestickInterval.MIN30, startTime=None, endTime=None, limit=2)
                #         break
                #     except:
                #         sleep(10)
                #         continue
                ticker_candles = request_client.get_candlestick_data(
                    symbol=ticker, interval=CandlestickInterval.MIN30, startTime=None, endTime=None, limit=2)
                # Записываем значения базовых показателей
                tickers_data[ticker]["O"].append(float(ticker_candles[0].open))
                tickers_data[ticker]["H"].append(float(ticker_candles[0].high))
                tickers_data[ticker]["L"].append(float(ticker_candles[0].low))
                tickers_data[ticker]["C"].append(float(ticker_candles[0].close))
                tickers_data[ticker]["V"].append(
                    int(float(ticker_candles[0].volume)))

                tickers_data[ticker]["O"].pop(0)
                tickers_data[ticker]["H"].pop(0)
                tickers_data[ticker]["L"].pop(0)
                tickers_data[ticker]["C"].pop(0)
                tickers_data[ticker]["V"].pop(0)
                
                tickers_data[ticker]["RSI"] = RSI(tickers_data[ticker]["C"], periods=14)

                # Получаем значения MACD, ее цвета и скользящие средние, используемые для расчета
                tickers_data[ticker]["MACD"], tickers_data[ticker]["MACD_Color"], tickers_data[ticker]["EMA12"], tickers_data[ticker]["EMA26"], tickers_data[ticker]["Signal"] = getMACD(tickers_data[ticker]["C"], 12, 26, 9)
                
                if ticker == "ARPAUSDT":
                    bot.send_message(message.chat.id, str(tickers_data[ticker]["C"][len(tickers_data[ticker]["C"])-1]))
                
            # Обнуляем текстовое сообщение 
            text_result = "M30 \n"
                    
            for ticker in my_tickers:
                if ticker == "ARPAUSDT":
                    bot.send_message(message.chat.id, str(tickers_data[ticker]["C"][len(tickers_data[ticker]["C"])-1]))
        
                macd_hist_3 = tickers_data[ticker]["MACD"][len(tickers_data[ticker]["C"])-3] - tickers_data[ticker]["Signal"][len(tickers_data[ticker]["C"])-3]
                macd_hist_2 = tickers_data[ticker]["MACD"][len(tickers_data[ticker]["C"])-2] - tickers_data[ticker]["Signal"][len(tickers_data[ticker]["C"])-2]
                macd_hist_1 = tickers_data[ticker]["MACD"][len(tickers_data[ticker]["C"])-1] - tickers_data[ticker]["Signal"][len(tickers_data[ticker]["C"])-1]
                # bot.send_message(message.chat.id, str(ticker) + " = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]))
                if ((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2] > 65) and (((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1] < tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2]) and (tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-3] < tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2])) or ((macd_hist_1 > 0) and (macd_hist_1 < macd_hist_2) and (macd_hist_3 < macd_hist_2)))):
                    if len(text_result) < 3700:
                        text_result += str(ticker) + " - ↧" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | " + '\n'
                    else:
                        bot.send_message(message.chat.id, text_result)
                        text_result = ""
                        text_result += str(ticker) + " - ↧" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | " + '\n'
                    # text_result += str(ticker) + " - ↧" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | " + '\n'
                elif ((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2] < 35) and (((tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1] > tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2]) and (tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-3] > tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-2])) or ((macd_hist_1 < 0) and (macd_hist_1 > macd_hist_2) and (macd_hist_2 < macd_hist_3)))):
                    if len(text_result) < 3700:
                        text_result += str(ticker) + " - ↥" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | "  + '\n'
                    else:
                        bot.send_message(message.chat.id, text_result)
                        text_result = ""
                        text_result += str(ticker) + " - ↥" + " | RSI = " + str(tickers_data[ticker]["RSI"][len(tickers_data[ticker]["C"])-1]) + " | "  + '\n'
            
            if text_result != "":     
                bot.send_message(message.chat.id, text_result)
                
bot.polling(none_stop=True, interval=0)