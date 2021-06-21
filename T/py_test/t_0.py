import cv2
import numpy as np
import random

# # 首先读入img
# img = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_19/liv.png', cv2.IMREAD_COLOR)
# img = cv2.resize(img, (180, 32))
# # N对基准控制点
# N = 5
# points = []
# dx = int(180 / (N - 1))
# for i in range(2 * N):
#     points.append((dx * i, 4))
#     points.append((dx * i, 36))
# # 周围拓宽一圈
# img = cv2.copyMakeBorder(img, 4, 4, 0, 0, cv2.BORDER_REPLICATE)
# # 画上绿色的圆圈
# for point in points:
#     cv2.circle(img, point, 1, (0, 255, 0), 2)
# tps = cv2.createThinPlateSplineShapeTransformer()
#
# sourceshape = np.array(points, np.int32)
# sourceshape = sourceshape.reshape(1, -1, 2)
# matches = []
# for i in range(1, N + 1):
#     matches.append(cv2.DMatch(i, i, 0))
#
# # 开始随机变动
# newpoints = []
# PADDINGSIZ = 10
# for i in range(N):
#     nx = points[i][0] + random.randint(0, PADDINGSIZ) - PADDINGSIZ / 2
#     ny = points[i][1] + random.randint(0, PADDINGSIZ) - PADDINGSIZ / 2
#     newpoints.append((nx, ny))
# print(points, newpoints)
# targetshape = np.array(newpoints, np.int32)
# targetshape = targetshape.reshape(1, -1, 2)
# tps.estimateTransformation(sourceshape, targetshape, matches)
# img = tps.warpImage(img)
# cv2.imwrite('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_19/tmp.png', img)

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
    if len(word2) == 0:
        return len(word1)
    if len(word1) == 0:
        return len(word2)

    dp = [[0 for _ in range(len(word2))] for _ in range(len(word1))]
    for i in range(len(word1)):
        for j in range(len(word2)):
            if word1[i] == word2[j]:
                if i == 0 and j == 0:
                    dp[i][j] = 0
                elif i == 0 and j != 0:
                    dp[i][j] = dp[i][j-1]
                elif j == 0 and i != 0:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i - 1][j - 1]
            else:
                if i == 0 and j == 0:
                    dp[i][j] = 1
                elif i == 0 and j != 0:
                    dp[i][j] = 1 + dp[i][j - 1]
                elif j == 0 and i != 0:
                    dp[i][j] = 1 + dp[i - 1][j]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])
    # dp = [[0 for _ in range(len(word2)+1)] for _ in range(len(word1)+1)]
    # for i in range(len(dp[0])):
    #     dp[0][i] = i
    # for i in range(len(dp)):
    #     dp[i][0] = i
    # for i in range(1, len(word1)+1):
    #     for j in range(1, len(word2)+1):
    #         if word1[i-1] == word2[j-1]:
    #             dp[i][j] = dp[i - 1][j - 1]
    #         else:
    #             dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])
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

