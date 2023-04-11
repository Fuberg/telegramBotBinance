from EMA import *
from SMA import *

# Функция для расчета MACD на всем графике 
def getMACD(C, first_Ema_Period, second_Ema_Period, signal_Period):

    EMA12 = getEMA(C, first_Ema_Period)
    EMA34 = getEMA(C, second_Ema_Period)
    # В этом массиве будут храниться значение, зеленая эта гистограмма или красная 
    MACD_Color = []
    MACD = []

    for i in range(0, len(C)):
        if EMA34[i] == 0.0:
            MACD.append(0.0)
            MACD_Color.append('R')
        else:
            # MACD_Point = ((EMA12[i] - EMA34[i]) / EMA34[i]) * 100
            MACD_Point = EMA12[i] - EMA34[i]
            MACD.append(round(MACD_Point, 6))
            MACD_Color.append('G' if MACD[i] > MACD[i-1] else 'R')
    
    Signal_Line = getEMA(C = MACD, period = signal_Period)

    return MACD, MACD_Color, EMA12, EMA34, Signal_Line

# TODO: сдописать нахожедие новой MACD 
def getLastMACD(C, MACD, MACD_Color, EMA12, EMA34, Signal_Line):
        EMA12 = getLastEMA(C, 12, EMA12)
        EMA34 = getLastEMA(C, 26, EMA34)
        MACD_Point = ((EMA12[len(EMA34)-1] - EMA34[len(EMA34)-1]) / EMA34[len(EMA34)-1]) * 100
        MACD.append(round(MACD_Point, 6))
        MACD_Color.append('G' if MACD[len(MACD)-1] > MACD[len(MACD)-2] else 'R')
        Signal_Line = getLastSMA(MACD, 9, Signal_Line)

        return MACD, MACD_Color, EMA12, EMA34, Signal_Line

