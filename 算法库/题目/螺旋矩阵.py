"""
    https://leetcode-cn.com/problems/spiral-matrix/
    54. 螺旋矩阵
    给你一个 m 行 n 列的矩阵 matrix ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。
    输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    输出：[1,2,3,4,8,12,11,10,9,5,6,7]
"""


def spiralOrder(matrix):
    h, w = len(matrix), len(matrix[0])
    up = 0
    down = h - 1
    left = 0
    right = w - 1

    out_list = []
    while True:
        out_list += [matrix[up][i] for i in range(left, right + 1)]
        up += 1
        if up > down:
            break
        out_list += [matrix[i][right] for i in range(up, down + 1)]
        right -= 1
        if left > right:
            break
        out_list += [matrix[down][i] for i in range(left, right + 1)][::-1]
        down -= 1
        if up > down:
            break
        out_list += [matrix[i][left] for i in range(up, down + 1)][::-1]
        left += 1
        if left > right:
            break
    return out_list


matrix = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]]
# matrix = [[1, 2, 3],
#           [4, 5, 6],
#           [7, 8, 9]]
print(spiralOrder(matrix))
