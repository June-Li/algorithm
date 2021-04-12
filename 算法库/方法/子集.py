def subset(nums, used_list, res):
    for index,  i in enumerate(nums):
        if i not in used_list:
            used_list.append(i)
            res.append(used_list.copy())
            subset(nums[index:], used_list, res)
            used_list.remove(i)


res = [[]]
nums = [1, 2, 3]
used_list = []
subset(nums, used_list, res)
print(res)

