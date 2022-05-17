def fun(n):
    if len(n) == 0:
        return 0
    i = 0
    for j in range(len(n)):
        if n[j] != n[i]:
            i += 1
            n[i] = n[j]
    return i+1


example = {
    0: [[1, 2, 2, 3, 3, 4], 4],
    1: [[1, 2], 2],
    2: [[], 0]
}
for key in example:
    out = fun(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')