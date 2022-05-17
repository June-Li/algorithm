def fun(nums):

    return 0


example = {
    0: [[3, 1, 5, 8], 167],
    1: [[1, 5], 10]
}
for key in example:
    out = fun(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')

