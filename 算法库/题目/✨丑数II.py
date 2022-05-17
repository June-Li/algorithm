def fun(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    p2 = p3 = p5 = 1

    for i in range(2, n + 1):
        num2, num3, num5 = dp[p2] * 2, dp[p3] * 3, dp[p5] * 5
        dp[i] = min(num2, num3, num5)
        if dp[i] == num2:  # 因为可能三个指针得到的值是相同的，所以用三个if，而不是if接elif
            p2 += 1
        if dp[i] == num3:
            p3 += 1
        if dp[i] == num5:
            p5 += 1

    return dp[n]


example = {
    0: [10, 12],
    1: [1, 1]
}
for key in example:
    out = fun(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')
