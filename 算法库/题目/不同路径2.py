def uniquePathsWithObstacles(obstacleGrid):
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [[1] * n] + [[1] + [0] * (n - 1) for _ in range(m - 1)]
    for i in range(n):
        if obstacleGrid[0][i] == 1:
            for j in range(i, n):
                dp[0][j] = 0
            break

    for j in range(m):
        if obstacleGrid[j][0] == 1:
            for i in range(j, m):
                dp[i][0] = 0

    for j in range(1, m):
        for i in range(1, n):
            if obstacleGrid[j][i] == 1 or ((dp[j][i - 1] == 0) and (dp[j - 1][i] == 0)):
                dp[j][i] = 0
            else:
                dp[j][i] = dp[j][i - 1] + dp[j - 1][i]
    return dp[-1][-1]


import numpy as np

# obstacleGrid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
# obstacleGrid = [[0, 1, 0], [1, 1, 0], [0, 0, 0]]
# obstacleGrid = [[0, 1], [0, 0]]
obstacleGrid = [[0, 1, 0], [1, 1, 0], [0, 0, 0], [0, 1, 0]]
print(uniquePathsWithObstacles(obstacleGrid))
