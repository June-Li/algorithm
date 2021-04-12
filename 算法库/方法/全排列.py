# 深度优先遍历（递归，回溯）
def AllRange(listx, start, end):
    if start == end:
        for i in listx:
            print(i, end='')
        print()
    for m in range(start, end + 1):
        listx[m], listx[start] = listx[start], listx[m]
        AllRange(listx, start + 1, end)
        listx[m], listx[start] = listx[start], listx[m]


list1 = [1, 2, 3]
AllRange(list1, 0, 2)


# 广度优先遍历
pass

