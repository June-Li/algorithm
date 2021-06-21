def minimumTotal(triangle):
    dp = triangle.copy()
    for i in range(len(triangle)):
        for j in range(len(triangle[i])):
            if i == 0:
                continue
            elif j == 0:
                dp[i][j] = dp[i-1][j] + triangle[i][j]
            elif i == j:
                dp[i][j] = dp[i - 1][j - 1] + triangle[i][j]
            else:
                dp[i][j] = min(dp[i-1][j], dp[i-1][j-1]) + triangle[i][j]
    return min(dp[-1])


triangle = [[2],
            [3, 4],
            [6, 5, 7],
            [4, 1, 8, 3]]
dp = minimumTotal(triangle)
print(dp)
# for i in dp:
#     print(i)
