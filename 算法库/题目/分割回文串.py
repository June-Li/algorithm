"""
方法介绍：
    先把找出所有的回文子串给找出来，然后遍历所有的回文子串，一个集合必须满足如下形式：
        eg：1-3，4-5，6-9，……
"""


def partition(s):
    def all_palindrome_str(ori_str):
        palindrome_list_ = []
        start_dict_ = {}
        dp_ = [[False for _ in range(len(ori_str))] for _ in range(len(ori_str))]
        dp_[0][0] = True
        # i表示行（区间右侧），j表示列（区间左侧）
        for i in range(len(dp_)):
            for j in range(i+1):
                if i - j == 0:
                    dp_[i][j] = True
                elif abs(i-j) == 1:
                    if s[i] == s[j]:
                        dp_[i][j] = True
                else:
                    if s[i] == s[j]:
                        dp_[i][j] = dp_[i-1][j+1]
                if dp_[i][j]:
                    palindrome_list_.append(s[j:i + 1])
                    if j in start_dict_.keys():
                        start_dict_[j].append([j, i])
                    else:
                        start_dict_[j] = []
                        start_dict_[j].append([j, i])

        return dp_, palindrome_list_, start_dict_
    dp, palindrome_list, start_dict = all_palindrome_str(s)

    partition_merge_str = []
    def search_fun(j, palindrome_sub):
        for sub_str in start_dict[j]:
            palindrome_sub.append(s[sub_str[0]:sub_str[1]+1])
            if sub_str[1] == len(s)-1:
                partition_merge_str.append(palindrome_sub.copy())
                palindrome_sub = palindrome_sub[:-1]
                return palindrome_sub
            if sub_str[1]+1 in start_dict.keys():
                palindrome_sub = search_fun(sub_str[1]+1, palindrome_sub)
            palindrome_sub = palindrome_sub[:-1]
        return palindrome_sub

    search_fun(0, [])
    return partition_merge_str


# s = "aab"
s = 'aafggfb'
# s = 'cbbbcc'
out = partition(s)
print(out)
print(len(out))
# [["a","a","b"],["aa","b"]]
