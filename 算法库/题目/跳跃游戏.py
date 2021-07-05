# def canJump(nums):
#     if len(nums) == 1:
#         return True
#     dp = [False for _ in range(len(nums))]
#     for index in range(len(nums) - 1):
#         start = index + 1
#         end = min(index+1 + nums[index], len(nums))
#         dp[start:end] = [True for _ in range(abs(start-end))]
#     return dp[-1]


def canJump(nums):
    if len(nums) == 1:
        return True

    length = len(nums)
    dp = [False for _ in range(len(nums))]
    dp[0] = True
    end = 1
    stop = 0
    while True:
        if end == length or stop == end:
            break
        if end > stop:
            tt = end
            for index, value in enumerate(dp[stop:end]):
                index += stop
                if value:
                    if index > 0 and nums[index] < nums[index-1]:
                        continue
                    start_ = index + 1
                    end_ = min(index+1 + nums[index], length)
                    dp[start_:end_] = [True for _ in range(abs(start_-end_))]
                    if end_ > end:
                        end = end_
            stop = tt

    return dp[-1]


# nums = [0, 2, 3]
# False
# nums = [0]
# True
# nums = [2, 3, 1, 1, 4]
# true
nums = [3, 2, 1, 0, 4]
# false
out = canJump(nums)
print(out)
