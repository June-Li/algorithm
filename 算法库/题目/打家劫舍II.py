# def rob(nums):
#     dp_select = [0 for _ in range(len(nums))]
#     dp_select[0] = nums[0]
#     dp_unselect = [0 for _ in range(len(nums))]
#     flag = False
#     if dp_select[0] > dp_unselect[0]:
#         flag = True
#     for i in range(1, len(nums)):
#         dp_select[i] = dp_unselect[i - 1] + nums[i]
#         dp_unselect[i] = max(dp_select[i - 1], dp_unselect[i - 1])
#     if flag and len(nums) > 1:
#         return dp_unselect[-1]
#     else:
#         return max(dp_select[-1], dp_unselect[-1])


# def rob(nums):
#     if len(nums) == 1:
#         return nums[0]
#     elif len(nums) == 2:
#         return max(nums)
#     dp_select = [0 for _ in range(len(nums))]
#     dp_select[1] = nums[0]
#     dp_unselect = [0 for _ in range(len(nums))]
#     dp_unselect[1] = dp_select[1]
#
#     for i in range(2, len(nums)):
#         dp_select[i] = dp_unselect[i - 1] + nums[i]
#         dp_unselect[i] = max(dp_select[i - 1], dp_unselect[i - 1])
#
#     if dp_select[-1] < dp_unselect[-1]:
#         return dp_select[-1]
#     else:
#         nums = nums[1:]
#         if len(nums) == 1:
#             return nums[0]
#         elif len(nums) == 2:
#             return max(nums)
#         dp_select = [0 for _ in range(len(nums))]
#         dp_select[1] = nums[0]
#         dp_unselect = [0 for _ in range(len(nums))]
#         dp_unselect[1] = dp_select[1]
#
#         for i in range(2, len(nums)):
#             dp_select[i] = dp_unselect[i - 1] + nums[i]
#             dp_unselect[i] = max(dp_select[i - 1], dp_unselect[i - 1])
#         return max(dp_select[-1], dp_unselect[-1])


def rob(nums):
    if len(nums) == 1:
        return nums[0]
    nums_1 = nums[0:-1]
    dp_select = [0 for _ in range(len(nums_1))]
    dp_select[0] = nums_1[0]
    dp_unselect = [0 for _ in range(len(nums_1))]

    for i in range(1, len(nums_1)):
        dp_select[i] = dp_unselect[i - 1] + nums_1[i]
        dp_unselect[i] = max(dp_select[i - 1], dp_unselect[i - 1])

    nums_2 = nums[1:]
    dp_select_ = [0 for _ in range(len(nums_2))]
    dp_select_[0] = nums_2[0]
    dp_unselect_ = [0 for _ in range(len(nums_2))]

    for i in range(1, len(nums_2)):
        dp_select_[i] = dp_unselect_[i - 1] + nums_2[i]
        dp_unselect_[i] = max(dp_select_[i - 1], dp_unselect_[i - 1])

    return max(max(dp_select[-1], dp_unselect[-1]), max(dp_select_[-1], dp_unselect_[-1]))


# nums = [1, 2, 3, 1]
# nums = [2, 7, 9, 3, 1]
# nums = [1, 2]
# nums = [2]
nums = [2, 2, 2, 5, 7]
print(rob(nums))
