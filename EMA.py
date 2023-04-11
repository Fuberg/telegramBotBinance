def getEMA(C, period):
    # Массив 
    ema = []
    # Проходимся по свечам 
    for index in range(0, (len(C))):
        # если свечей недостаточно для расчета, то мы возвращаем 0
        if index < (period-2):
            ema.append(0.0)
        # если мы сейчас последней свече, на которой нам нехватает свечей для расчета, то 
        # мы возвращаем Close текущей свечи 
        elif index == (period-2):
            ema.append(C[index])
        # Когда свечей достаточно, мы производим расчет по формуле, а потом возвращаем значение, но
        # забиваем его с округлением до 6 знаков после запятой
        else:
            ema_point = ((ema[index-1] * (period-1)) + (2 * C[index]))/(period+1)
            ema.append(round(ema_point,6))
    
    # Возвращаем массив значений EMA 
    return ema 

def getLastEMA(C, period, EMA):
        ema_point = ((EMA[len(EMA)-1] * (period-1)) + (2 * C))/(period+1)
        EMA.append(round(ema_point,6))
        return EMA

# def toFixed(numObj, digits=0):
#     return float(f"{numObj:.{digits}f}")