"""
v0：超时
"""


def maxProduct_v0(nums):
    nums_len = len(nums)
    dp = [nums.copy() for _ in nums]
    max_p = max(nums)
    for i in range(1, nums_len):
        for j in range(i):
            if abs(i - j) > 2:
                dp[i][j] = nums[i] * nums[j] * dp[i - 1][j + 1]
            elif abs(i - j) > 1:
                dp[i][j] = nums[i] * nums[j] * nums[i - 1]
            else:
                dp[i][j] = nums[i] * nums[j]
            if dp[i][j] > max_p:
                max_p = dp[i][j]

    return max_p


def maxProduct_v1(nums):
    nums_len = len(nums)
    dp_max, dp_min = nums.copy(), nums.copy()
    for i in range(1, nums_len):
        dp_max[i] = max(dp_max[i - 1] * nums[i], nums[i], dp_min[i - 1] * nums[i])
        dp_min[i] = min(dp_min[i - 1] * nums[i], nums[i], dp_max[i - 1] * nums[i])

    return max(dp_max)


def maxProduct_v2(nums):
    nums_len = len(nums)
    max_p, dp_max_pre, dp_min_pre = nums[0], nums[0], nums[0]
    for i in range(1, nums_len):
        dp_max_pre_temp = max(dp_max_pre * nums[i], nums[i], dp_min_pre * nums[i])
        dp_min_pre = min(dp_min_pre * nums[i], nums[i], dp_max_pre * nums[i])
        dp_max_pre = dp_max_pre_temp
        max_p = max(max_p, dp_max_pre)

    return max_p


example = {
    0: [[0, 2], 2],
    1: [[2, 3, -2, 4], 6],
    2: [[-2, 0, -1], 0],
    3: [[-2, 1, -1], 2],
    4: [[-1, -2, -9, -6], 108],
    5: [[2, 3, -2, 4, 5, 1, 0, 2, 6, 1, 0, 1, 5, 2], 20],
    6: [[2, 3, -2, 4], 6]
}
for key in example:
    out = maxProduct_v2(example[key][0])
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')
