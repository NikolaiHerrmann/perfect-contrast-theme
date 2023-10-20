def func1(list=[3, 4, 5, 99, 1]):
    count = 0

    for x in list:
        if x % 2 == 0:
            count += 1
        else:
            count -= 1

    return count

def func2(list=[2, 5, 55, 6, 100]):
    count = 0

    for x in list:
        if x % 5 == 0:
            count += 1
        else:
            count -= 1

    return count

def func3(list=[4, 7, 55, 16, 77]):
    count = 0

    for x in list:
        if x % 2 == 0:
            count += 1
        else:
            count -= 1
    
    return count

def func4(list=[5, 8, 33, 3, 9]):
    count = 0

    for x in list:
        if x % 3 == 0:
            count += 1
        else:
            count -= 1

    return count

def func5(list=[9, 9, 55, 1, 5]):
    count = 0

    for x in list:
        if x % 5 == 0:
            count += 1
        else:
            count -= 1

    return count

def func6(list=[7, 9, 4, 5, 3]):
    count = 0

    for x in list:
        if x % 2 == 0:
            count += 1
        else:
            count -= 1
    
    return count
