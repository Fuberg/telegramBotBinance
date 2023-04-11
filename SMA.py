# getSMA("Цены закрытия", "Период", "Массив с уже имеющимеся данными SMA", "Нужны ли границы", "Какой должен быть процент граиниц")
def getSMA(C = [], period = 10):

    SMA = []
    # index нужен, чтобы перебирать все свечи 
    index = 0
    # Для подсчета суммы
    sum = 0.0
    # Переменные в которых храняться границы SMA 10 
    top_border = []
    bot_border = []
    # Проходимся по всем свечам 
    while index < len(C):
        # Если пока не хватает свечей для вычисления пишем 0
        if index < (period-1):
            SMA.append(0.0)
        else:
            # Проходим по всем свечам в зависимости о периода и складываем их в sum 
            for i in range((index + 1) - period, (index + 1)):
                sum = sum + C[i]

            # Добавляем среднее значение 
            SMA.append(sum/period)

            # Зануляем sum для дальнейших итерация вычислений 
            sum = 0
        
        index += 1

    return SMA

def getLastSMA(C, period, SMA):
    last_point = len(C) - 1
    sum = 0.0 
    for i in range((last_point - period), last_point):
        sum = sum + C[i]
    SMA.append(sum/period)
    return SMA



#   get_sma_point ("цены закрытия", "Период", "В какой точке надо расчитать SMA 
#   (index надо указывать на один меньше номера свечи, потому что в массиве значения идут с нулевого элемента)")
def get_sma_point (C, period, index = 0):
    if index == 0 : 
        index = period - 1

    sum = 0.0
    for i in range(((index + 1) - period), (index + 1)):
        sum = sum + C[i]
    
    return sum/period



