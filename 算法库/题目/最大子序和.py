import time
import numpy as np
"""
动态规划：时间溢出
"""
def maxSubArray(nums):
    length = len(nums)
    max_ = max(nums)
    temp = [None for _ in range(length)]
    dp = [temp.copy() for _ in range(length)]

    for i in range(length):
        dp[i][i] = nums[i]
    for j in range(length):
        for i in range(0, j):
            if abs(i-j) == 1:
                dp[j][i] = nums[i] + nums[j]
            else:
                dp[j][i] = nums[i] + nums[j] + dp[j-1][i+1]
            max_ = max(dp[j][i], max_)

    return max_


"""
动态规划：时间未溢出
思路：
    遍历nums，求以第i个结尾的子序列的值，只有前[x, i-1]个数大于0才有增益，值得加，如果前[x, i-1]小于0就没必要加了，因为需要增益，还要连续，所以就没必要了，具体如下：
        dp[i]表示nums中以nums[i]结尾的最大子序和
        dp[0] = nums[0]
        dp[i] = max(dp[i- 1] + nums[i], nums[i]);
"""
# def maxSubArray(nums):
#     max_ = nums[0]
#     sum = 0
#     for num in nums:
#         if sum > 0:
#             sum += num
#         else:
#             sum = num
#         max_ = max(max_, sum)
#     return max_


"""
分治
"""
# def maxSubArray(nums):
#     n = len(nums)
#     # 递归终止条件
#     if n == 1:
#         return nums[0]
#     else:
#         # 递归计算左半边最大子序和
#         max_left = maxSubArray(nums[0:len(nums) // 2])
#         # 递归计算右半边最大子序和
#         max_right = maxSubArray(nums[len(nums) // 2:len(nums)])
#
#     # 计算中间的最大子序和，从右到左计算左边的最大子序和，从左到右计算右边的最大子序和，再相加
#     max_l = nums[len(nums) // 2 - 1]
#     tmp = 0
#     for i in range(len(nums) // 2 - 1, -1, -1):
#         tmp += nums[i]
#         max_l = max(tmp, max_l)
#     max_r = nums[len(nums) // 2]
#     tmp = 0
#     for i in range(len(nums) // 2, len(nums)):
#         tmp += nums[i]
#         max_r = max(tmp, max_r)
#     # 返回三个中的最大值
#     return max(max_right, max_left, max_l + max_r)


def main():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]  # *1000
    # nums = [-2, 1]
    start = time.time()
    max_ = maxSubArray(nums)
    print('use time: ', time.time() - start)
    print(max_)


if __name__ == '__main__':
    main()
