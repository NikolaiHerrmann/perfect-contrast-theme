def func1(list1=[3, -1], list2=[66, 7]):

    list3 = list1 + list2
    list3[1] += 1
    list3[3] = list1[0]
    
    return list3[1] + list3[3]

def func2(list1=[5, 7], list2=[2, 3]):

    list3 = list1 + list2
    list3[2] += 2
    list3[3] = list2[1]

    return list3[2] + list3[3]

def func3(list1=[2, 4], list2=[99, 1]):

    list3 = list1 + list1
    list3[2] += 2
    list3[1] = list3[0]

    return list3[2] + list3[1]

def func4(list1=[-2, -1], list2=[-1, -2]):

    list3 = list2 + list1
    list3[1] += 1
    list3[0] = list3[1]

    return list3[0] + list3[1]

def func5(list1=[5, 5], list2=[6, 6]):
    
    list3 = list2 + list2
    list3[0] -= 6
    list3[3] = list3[0]

    return list3[0] + list3[3]

def func6(list1=[1, 2], list2=[3, 4]):
    
    list3 = list1 + list2
    list3[0] -= 2 
    list3[2] = list3[1]

    return list3[2] + list3[3]
