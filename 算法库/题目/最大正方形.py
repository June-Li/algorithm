def maximalSquare(matrix):
    max_v = 0
    for idx_1, _ in enumerate(matrix):
        for idx_2, _ in enumerate(matrix[0]):
            if idx_1 == 0 or idx_2 == 0 or matrix[idx_1][idx_2] == '0':
                max_v = max(max_v, int(matrix[idx_1][idx_2]))
                continue
            matrix[idx_1][idx_2] = min(int(matrix[idx_1][idx_2 - 1]),
                                       int(matrix[idx_1 - 1][idx_2]),
                                       int(matrix[idx_1 - 1][idx_2 - 1]))+1
            max_v = max(max_v, matrix[idx_1][idx_2])

    return max_v**2


example = {
    # 0: [[["0", "1"], ["1", "0"]], 1],
    # 1: [[["0"]], 0],
    2: [[["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]], 4]
}
for key in example:
    out = maximalSquare(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')
