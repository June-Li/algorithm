def fun(prices):
    if not prices:
        return 0

    n = len(prices)
    # f[i][0]: 手上持有股票的最大收益
    # f[i][1]: 手上不持有股票，并且处于冷冻期中的累计最大收益
    # f[i][2]: 手上不持有股票，并且不在冷冻期中的累计最大收益
    f = [[-prices[0], 0, 0]] + [[0] * 3 for _ in range(n - 1)]
    for i in range(1, n):
        f[i][0] = max(f[i - 1][0], f[i - 1][2] - prices[i])
        f[i][1] = f[i - 1][0] + prices[i]
        f[i][2] = max(f[i - 1][1], f[i - 1][2])

    return max(f[n - 1][1], f[n - 1][2])


example = {
    0: [[1, 2, 3, 0, 2], 3]
}
for key in example:
    out = fun(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')

