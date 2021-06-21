def rob(nums):
    dp_select = [0 for _ in range(len(nums))]
    dp_select[0] = nums[0]
    dp_unselect = [0 for _ in range(len(nums))]

    for i in range(1, len(nums)):
        dp_select[i] = dp_unselect[i - 1] + nums[i]
        dp_unselect[i] = max(dp_select[i - 1], dp_unselect[i - 1])

    return max(dp_select[-1], dp_unselect[-1])


# nums = [1, 2, 3, 1]
nums = [2, 7, 9, 3, 1]
# nums = [2]
# nums = [2, 2, 2, 5, 7]
out = rob(nums)
print(out)

