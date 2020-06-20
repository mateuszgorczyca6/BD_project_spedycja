from math import floor

def working_day(date):
    d, m, y = date.day, date.month, date.day
    def day_of_week(day, month, year):
        t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
        year -= month < 3
        return (year + int(year/4) - int(year/100) + int(year/400) + t[month-1] + day) % 7

    def to_Easter(dd, mm, yy):
        # data wielkanocy
        a = yy % 19
        b = floor(yy / 100)
        c = yy % 100
        d = floor(b / 4)
        e = b % 4
        f = floor((b + 8) / 25)
        g = floor((b - f + 1) / 3)
        h = (19 * a + b - d - g + 15) % 30
        i = floor(c / 4)
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = floor((a + 11 * h + 22 * l) / 451)
        p = (h + l - 7 * m + 114) % 31
        wd = p + 1
        wm = floor((h + l - 7 * m + 114) / 31)
        # liczba dni w miesiącu
        mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if yy % 4 == 0 and (yy % 100 > 0 or yy % 400 == 0):
            mdays[1] = 29
        # dzień w roku wielkanocy
        windays = wd + sum(mdays[:wm - 1])
        # dzień w roku podanej daty
        ddays = dd
        if mm >0:
            ddays += sum(mdays[:mm - 1])
        return windays - ddays
    
    # # # weekendy # # #
    if day_of_week in [6, 7]:
        return False
    
    # # # święta # # #
    # https://www.kalendarzswiat.pl/swieta/2019
    if m == 1 and d in [1, 6]:
        return False
    # Nowy Rok - 1 stycznia
    # Trzech Króli - 6 stycznia
    if m == 2 and d in [2]:
        return False
    # Ofiarowanie Pańskie - 2 luty
    if m == 5 and d in [1, 3]:
        return False
    # Święto Pracy - 1 maja
    # Święto Konstytucji 3 maja - 3 maja
    if m == 11 and d in [1, 11]:
        return False
    # Wszystkich Świętych - 1 listopada
    # Narodowe święto Niepodległości - 11 listopada
    if m == 12 and d in [24, 25, 26]:
        return False
    # Wigilia - 24 grudnia
    # Boże Narodzenie - 25-26 grudnia
    if to_Easter(d, m, y) in [0, -1, -60]:
        return False
    # wielkanoc
    # poniedziałek wielkanocny - 1 dzień po wielkanocy
    # boże ciało - 60 dni po wielkanocy
    # pominięte zostały święta weekendowe

    return True