def fun(n):

    return 0


example = {
    0: [[], []],
    1: [[], []]
}
for key in example:
    out = fun(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')
