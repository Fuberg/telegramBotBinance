def RSI(C, periods=14):
    length = len(C)
    rsi = [0.0]*length
    up_avg = [0.0]*length
    down_avg = [0.0]*length
    # Длина данных не превышает периода и не может быть рассчитана;
    if length <= periods:
        return rsi
        # Используется для быстрого расчета;
    
    for i in range(2, len(C)):
        avg = C[i] - C[i-1]
        up_avg[i] = avg if avg > 0.0 else 0.0
        down_avg[i] = (avg * -1) if avg < 0.0 else 0.0
    
    up = pine_rma(up_avg, periods)
    down = pine_rma(down_avg, periods)
    
    for i in range(2, len(C)):
        if down[i] == 0.0:
            rsi[i] = 100.0
        elif up[i] == 0.0:
            rsi[i] = 0.0
        else:
            rsi[i] = round((100 - (100 / (1 + (up[i] / down[i])))),2)
        
    return rsi

def pine_rma(src, period):
    length = len(src)
    alpha = 1/period
    rma = [0.0]*length
    for i in range(2, length):
        if i < period:
            continue
        elif i == period:
            rma[i] = getSMA(src[-14:], period)
        else:
            rma[i] = alpha * src[i] + (1 - alpha) * rma[i-1]
    return rma
    
def getSMA(C, period):
    sum = 0.0
    for i in range(1, period):
        sum = sum + C[i]
       
    return sum/period