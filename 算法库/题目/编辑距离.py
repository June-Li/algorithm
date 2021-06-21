def minDistance_guanfang(word1, word2):
    n = len(word1)
    m = len(word2)

    # 有一个字符串为空串
    if n * m == 0:
        return n + m

    # DP 数组
    D = [[0] * (m + 1) for _ in range(n + 1)]

    # 边界状态初始化
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j

    # 计算所有 DP 值
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            left = D[i - 1][j] + 1
            down = D[i][j - 1] + 1
            left_down = D[i - 1][j - 1]
            if word1[i - 1] != word2[j - 1]:
                left_down += 1
            D[i][j] = min(left, down, left_down)

    return D[n][m]


def minDistance_my(word1, word2):
    # if len(word2) == 0:
    #     return len(word1)
    # if len(word1) == 0:
    #     return len(word2)
    #
    # dp = [[0 for _ in range(len(word2))] for _ in range(len(word1))]
    # for i in range(len(word1)):
    #     for j in range(len(word2)):
    #         if word1[i] == word2[j]:
    #             if i == 0 and j == 0:
    #                 dp[i][j] = 0
    #             elif i == 0 and j != 0:
    #                 dp[i][j] = dp[i][j-1]
    #             elif j == 0 and i != 0:
    #                 dp[i][j] = dp[i-1][j]
    #             else:
    #                 dp[i][j] = dp[i - 1][j - 1]
    #         else:
    #             if i == 0 and j == 0:
    #                 dp[i][j] = 1
    #             elif i == 0 and j != 0:
    #                 dp[i][j] = 1 + dp[i][j - 1]
    #             elif j == 0 and i != 0:
    #                 dp[i][j] = 1 + dp[i - 1][j]
    #             else:
    #                 dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])
    dp = [[0 for _ in range(len(word2)+1)] for _ in range(len(word1)+1)]
    for i in range(len(dp[0])):
        dp[0][i] = i
    for i in range(len(dp)):
        dp[i][0] = i
    for i in range(1, len(word1)+1):
        for j in range(1, len(word2)+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])
    return dp[-1][-1]


# word1 = "horse"
# # word1 = "rosl"
# word2 = "ros"
# word1 = "intention"
# word2 = "execution"
# word1 = 'sea'
# word2 = 'eat'
word1 = "pneumonoultramicroscopicsilicovolcanoconiosis"
word2 = "ultramicroscopically"
num = minDistance_my(word1, word2)
# num = minDistance_guanfang(word1, word2)
print(num)
