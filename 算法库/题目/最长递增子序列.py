def fun(nums):
    rec = []
    max_g = 1
    for idx, ele in enumerate(nums):
        if idx == 0:
            rec.append(1)
            continue
        max_v = 1
        for idx_1, ele_1 in enumerate(rec):
            if nums[idx_1] < ele and ele_1 >= max_v:
                max_v = ele_1 + 1
        rec.append(max_v)
        if max_v > max_g:
            max_g = max_v
    return max_g


example = {
    0: [[10, 9, 2, 5, 3, 7, 101, 18], 4],
    1: [[0, 1, 0, 3, 2, 3], 4],
    2: [[7, 7, 7, 7, 7, 7, 7], 1],
    3: [[2, 3, 1, 6, 8, 3, 9], 5]
}
for key in example:
    out = fun(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')
