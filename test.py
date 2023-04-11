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
                                                         startTime=None, endTime=None, limit=1500)
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

    tickers_data[ticker]["SIGNAL"] = [''] * len(tickers_data[ticker]["C"])
    tickers_data[ticker]["RESULT"] = [''] * len(tickers_data[ticker]["C"])

# Получаем значение SMA для каждой валютной пары
    # tickers_data[ticker]["SMA10"] = getSMA(tickers_data[ticker]["C"], 10)
    # tickers_data[ticker]["EMA21"] = getEMA(tickers_data[ticker]["C"], 21)
    # tickers_data[ticker]["EMA50"] = getEMA(tickers_data[ticker]["C"], 50)

    # # # Получаем значение фракталов
    # tickers_data[ticker]["Fractals_Max"], tickers_data[ticker]["Fractals_Min"] = getFractals(
    #     tickers_data[ticker]["H"], tickers_data[ticker]["L"])


for ticker in my_tickers[:]:
    if ((len(tickers_data[ticker]["C"]) < 1499) or ((tickers_data[ticker]["V"][len(tickers_data[ticker]["C"])-1]*tickers_data[ticker]["C"][len(tickers_data[ticker]["C"])-1]) < 1000000.0)):
        del tickers_data[ticker]
        my_tickers.remove(ticker)


# Проверяем, надо ли совершать сделаку, если да, то пишем ее данные
# for ticker in my_tickers:
for i in range(0, 1499):
    # Первые 500 свечей мы пропускаем, в том числе, чтобы все индикаторы точно правильно расчитались
    if i < 500:
        continue
    
    print(tickers_data["BTCUSDT"]["RSI"][i])

#         if i == 1499:
#             break

#         # if (((tickers_data[ticker]["EMA21"][i-1] < tickers_data[ticker]["SMA10"][i-1]) or (tickers_data[ticker]["EMA50"][i-1] < tickers_data[ticker]["EMA21"][i-1])) and (tickers_data[ticker]["EMA21"][i] > tickers_data[ticker]["SMA10"][i]) and (tickers_data[ticker]["EMA50"][i] > tickers_data[ticker]["EMA21"][i])):
#         #     if (tickers_data[ticker]["RSI"][i] < 50):
#         #         tickers_data[ticker]["SIGNAL"][i] = 'Продавай'

#         # if (((tickers_data[ticker]["EMA21"][i-1] > tickers_data[ticker]["SMA10"][i-1]) or (tickers_data[ticker]["EMA50"][i-1] > tickers_data[ticker]["EMA21"][i-1])) and (tickers_data[ticker]["EMA21"][i] < tickers_data[ticker]["SMA10"][i]) and (tickers_data[ticker]["EMA50"][i] < tickers_data[ticker]["EMA21"][i])):
#         #     if (tickers_data[ticker]["RSI"][i] > 50):
#         #         tickers_data[ticker]["SIGNAL"][i] = 'Покупай'

#         if ((tickers_data[ticker]["EMA50"][i-1] < tickers_data[ticker]["EMA21"][i-1]) and (tickers_data[ticker]["EMA50"][i] > tickers_data[ticker]["EMA21"][i])):
#             if (tickers_data[ticker]["RSI"][i] < 30):
#                 tickers_data[ticker]["SIGNAL"][i] = 'Продавай'

#         if ((tickers_data[ticker]["EMA50"][i-1] > tickers_data[ticker]["EMA21"][i-1]) and (tickers_data[ticker]["EMA50"][i] < tickers_data[ticker]["EMA21"][i])):
#             if (tickers_data[ticker]["RSI"][i] > 70):
#                 tickers_data[ticker]["SIGNAL"][i] = 'Покупай'

# all_plus_counter = 0
# all_minus_counter = 0
# total = 0.0

# # Проверяем, надо ли совершать сделаку, если да, то пишем ее данные
# for ticker in my_tickers:
#     ticker_plus_counter = 0
#     ticker_minus_counter = 0
#     ticker_total = 0.0

#     for i in range(0, 1499):
#         # Первые 500 свечей мы пропускаем, в том числе, чтобы все индикаторы точно правильно расчитались
#         if i < 500:
#             continue

#         if i == 1499:
#             break

#         position_open = 0.0

#         if (tickers_data[ticker]["SIGNAL"][i] == 'Продавай'):
#             position_open = tickers_data[ticker]["C"][i]
#             for j in range(i+1, 1499):
#                 # if ((tickers_data[ticker]["EMA21"][j] < tickers_data[ticker]["SMA10"][j]) or (tickers_data[ticker]["EMA50"][j] < tickers_data[ticker]["EMA21"][j])):
#                 if (tickers_data[ticker]["EMA50"][j] < tickers_data[ticker]["EMA21"][j]):
#                     tickers_data[ticker]["RESULT"][i] = (
#                         ((tickers_data[ticker]["C"][j]*100)/position_open)-100.0)*(-1)
#                     if (tickers_data[ticker]["RESULT"][i] >= 0.0):
#                         all_plus_counter += 1
#                         ticker_plus_counter += 1
#                     else:
#                         all_minus_counter += 1
#                         ticker_minus_counter += 1
#                     total += tickers_data[ticker]["RESULT"][i]
#                     ticker_total += tickers_data[ticker]["RESULT"][i]
#                     if ((i > 1495) and (ticker_total > 20.0)):
#                         print(ticker + " : Продавай")
#                     break

#         if (tickers_data[ticker]["SIGNAL"][i] == 'Покупай'):
#             position_open = tickers_data[ticker]["C"][i]
#             for j in range(i+1, 1499):
#                 # if ((tickers_data[ticker]["EMA21"][j] > tickers_data[ticker]["SMA10"][j]) or (tickers_data[ticker]["EMA50"][j] > tickers_data[ticker]["EMA21"][j])):
#                 if (tickers_data[ticker]["EMA50"][j] > tickers_data[ticker]["EMA21"][j]):
#                     tickers_data[ticker]["RESULT"][i] = (
#                         (tickers_data[ticker]["C"][j]*100)/position_open)-100.0
#                     if (tickers_data[ticker]["RESULT"][i] >= 0.0):
#                         all_plus_counter += 1
#                         ticker_plus_counter += 1
#                     else:
#                         all_minus_counter += 1
#                         ticker_minus_counter += 1
#                     total += tickers_data[ticker]["RESULT"][i]
#                     ticker_total += tickers_data[ticker]["RESULT"][i]
#                     if ((i > 1495) and (ticker_total > 20.0)):
#                         print(ticker + " : Покупай")
#                     break

#     rsi_control = False
#     for rsi in tickers_data[ticker]["RSI"][-6:]:
#         if ((rsi >= 70) or (rsi <= 30)):
#             rsi_control = True
#     if rsi_control:
#         print(ticker + " (+): " + str(ticker_plus_counter) + " | " + ticker + " (-): " +
#               str(ticker_minus_counter) + " | " + ticker + " Total(%): " + str(ticker_total) + "\n")

# Записываем нужные показатели в файл, у каждой пары свой файл
# for ticker in my_tickers:
#     f = open(("reports/" + str(ticker) + ".txt"), 'w')
#     for i in range(0, len(tickers_data[ticker]["O"])):
#         f.write(str(i) + ". " + " | Open:" + str(tickers_data[ticker]["O"][i]) + " | Close:" + str(tickers_data[ticker]["C"][i]) + " | High:" + str(tickers_data[ticker]["H"][i]) + " | Low:" + str(
#             tickers_data[ticker]["L"][i]) + " | RSI:" + str(tickers_data[ticker]["RSI"][i]) + " | Signal:" + str(tickers_data[ticker]["SIGNAL"][i]) + " | RESULT:" + str(tickers_data[ticker]["RESULT"][i]) + "\n")
        # f.write(str(i) + ". " + str(tickers_data[ticker]["profit"][i]) + " = " + str(tickers_data[ticker]["profit_direction"][i]) + "\t| Open:" + str(tickers_data[ticker]["O"][i]) + " | Close:" + str(tickers_data[ticker]["C"][i]) +  " | High:" + str(tickers_data[ticker]["H"][i]) +  " | Low:" + str(tickers_data[ticker]["L"][i]) +  " | Maximum:" + str(tickers_data[ticker]["Fractals_Max"][i]) + " | Minimum:" + str(tickers_data[ticker]["Fractals_Min"][i]) + " | SMA10:" + str(tickers_data[ticker]["SMA10"][i]) + " | EMA21:" + str(tickers_data[ticker]["EMA21"][i]) + " | EMA50:" + str(tickers_data[ticker]["EMA50"][i]) + "\n")
        # f.write(str(i) + ". " + " | Open:" + str(tickers_data[ticker]["O"][i]) + " | Close:" + str(tickers_data[ticker]["C"][i]) +  " | High:" + str(tickers_data[ticker]["H"][i]) +  " | Low:" + str(tickers_data[ticker]["L"][i]) +  " | Maximum:" + str(tickers_data[ticker]["Fractals_Max"][i]) + " | Minimum:" + str(tickers_data[ticker]["Fractals_Min"][i]) + " | SMA10:" + str(tickers_data[ticker]["SMA10"][i]) + " | Take-Profit:" + str(tickers_data[ticker]["Take-Profit"][i]) + " | STOP:" + str(tickers_data[ticker]["STOP"][i]) + "\n")

# print("Done")
# print("All (+) : " + str(all_plus_counter))
# print("All (-) : " + str(all_minus_counter))
# print("Total (%) : " + str(total))


# and (((tickers_data[ticker]["SMA10"][i-1] >= tickers_data[ticker]["EMA21"][i-1]) and (tickers_data[ticker]["EMA21"][i-1] >= tickers_data[ticker]["EMA50"][i-1]))
#  or ((tickers_data[ticker]["SMA10"][i-1] < tickers_data[ticker]["EMA21"][i-1]) and (tickers_data[ticker]["EMA21"][i-1] < tickers_data[ticker]["EMA50"][i-1])))
