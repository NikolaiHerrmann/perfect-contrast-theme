def func1(list=[4, 5, 3], n=3):
    m = 0

    for x in list:
        if x > n:
            m = x
        m -= 1
    
    return m

def func2(list=[45, 68, 64], n=67):
    m = 0

    for x in list:
        if x < n:
            m = 0
        m -= 1

    return m

def func3(list=[6, 6, 8], n=6):
    m = 0

    for x in list:
        if x == n:
            m = 0
        m -= 2

    return m

def func4(list=[7, 8, 4], n=7):
    m = 0

    for x in list:
        if x >= n:
            m -= 1
        m -= 1

    return m

def func5(list=[2, 3, 1], n=2):
    m = 0

    for x in list:
        if x >= n:
            m -= n
        m += 1

    return m

def func6(list=[6, 5, 7], n=6):
    m = 0

    for x in list:
        if x == n:
            n -= 1
        m += 2

    return m

