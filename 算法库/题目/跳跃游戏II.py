"""
my：超时
"""

def canJump(nums):
    length = len(nums)
    if length == 1:
        return 0

    dp_m = []

    for index, value in enumerate(nums):
        start_ = index + 1
        end_ = min(index+1 + nums[index], length)
        dp_m.append(list(range(start_, end_)))

    dp_min = [999999 for _ in range(len(nums))]
    dp_min[0] = 0
    for index in range(1, len(dp_min)):
        lie = [index_1 for index_1, i in enumerate(dp_m) if index in dp_m[index_1]]
        min_v = 999999
        for index_2 in lie:
            if dp_min[index_2] < min_v:
                min_v = dp_min[index_2]
        dp_min[index] = min_v+1

    return dp_min[-1]


"""
官方：有正向和反向两种方法，具体看官网介绍；
"""

# nums = [0]
# 0
# nums = [2, 3, 1, 1, 4]
# 2
# nums = [2,3,0,1,4]
# 2
nums = [3,1,1,1,1]
# 2
out = canJump(nums)
print(out)
