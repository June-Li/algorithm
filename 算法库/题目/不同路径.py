"""
方法1：动态规划
"""
# def uniquePaths(m, n):
#     dp = [[1] * n] + [[1] + [0] * (n - 1) for _ in range(m - 1)]
#
#     for j in range(1, m):
#         for i in range(1, n):
#             dp[j][i] = dp[j][i - 1] + dp[j - 1][i]
#     return dp[-1][-1]


"""
方法2：排列组合
"""
def uniquePaths(m, n):
    import math
    return int(math.factorial(m + n - 2) / math.factorial(m - 1) / math.factorial(n - 1))


# m = 3
# n = 7

m = 3
n = 2

print(uniquePaths(m, n))
