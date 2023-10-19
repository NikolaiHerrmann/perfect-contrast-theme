def func1(list1=[3, -1], list2=[66, 7]):
    list3 = []

    list3 = list1 + list2
    list3[1] += 1
    list3[3] = list1[0]
    
    return list3[1] + list3[3]

def func2(list1=[5, 7], list2=[2, 3]):
    list3 = []

    list3 = list1 + list2
    list3[2] += 2
    list3[3] = list2[1]

    return list3[2] + list3[3]

def func3(list1=[2, 4], list2=[99, 1]):
    list3 = []

    list3 = list1 + list1
    list3[2] += 2
    list3[1] = list3[0]

    return list3[2] + list3[1]

def func4(list=[4, 5, 55]):
    count = 0
    for x in list:
        count += 1 if x % 2 == 0 else -1
    return count

def func5(list=[4, 5, 55]):
    count = 0
    for x in list:
        count += 1 if x % 2 == 0 else -1
    return count

def func6(list=[4, 5, 55]):
    count = 0
    for x in list:
        count += 1 if x % 2 == 0 else -1
    return count

