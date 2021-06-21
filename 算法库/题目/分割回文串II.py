"""
方法介绍：
    先把找出所有的回文子串给找出来，然后遍历所有的回文子串，一个集合必须满足如下形式：
        eg：1-3，4-5，6-9，……
"""


def partition(s):
    def all_palindrome_str(ori_str):
        dp_ = [[False for _ in range(len(ori_str))] for _ in range(len(ori_str))]
        dp_num_ = [[0 for _ in range(len(ori_str))] for _ in range(len(ori_str))]
        # i表示行（区间右侧），j表示列（区间左侧）
        for i in range(len(dp_)):
            for j in range(i+1):
                if i - j == 0:
                    dp_[i][j] = True
                    if i == j == 0:
                        dp_num_[i][j] = 1
                    else:
                        if j == 0:
                            dp_num_[i][j] = 1
                        else:
                            [dp_num_[j - 1].remove(0) for _ in range(dp_num_[j - 1].count(0))]
                            if len(dp_num_[j - 1]) > 0:
                                dp_num_[i][j] = min(dp_num_[j - 1]) + 1
                            else:
                                dp_num_[i][j] = 0
                elif abs(i-j) == 1:
                    if s[i] == s[j]:
                        dp_[i][j] = True
                        if j == 0:
                            dp_num_[i][j] = 1
                        else:
                            [dp_num_[j - 1].remove(0) for _ in range(dp_num_[j - 1].count(0))]
                            if len(dp_num_[j - 1]) > 0:
                                dp_num_[i][j] = min(dp_num_[j - 1]) + 1
                            else:
                                dp_num_[i][j] = 0
                else:
                    if s[i] == s[j]:
                        dp_[i][j] = dp_[i-1][j+1]
                        if dp_[i][j]:
                            if j == 0:
                                dp_num_[i][j] = 1
                            else:
                                [dp_num_[j - 1].remove(0) for _ in range(dp_num_[j - 1].count(0))]
                                if len(dp_num_[j - 1]) > 0:
                                    dp_num_[i][j] = min(dp_num_[j - 1])+1
                                else:
                                    dp_num_[i][j] = 0

        return dp_num_
    dp_num = all_palindrome_str(s)
    [dp_num[-1].remove(0) for _ in range(dp_num[-1].count(0))]

    return min(dp_num[-1])-1


# s = "aab"
s = 'aafggfb'
# s = 'cbbbcc'
# s = "ababababababababababababcbabababababababababababa"
out = partition(s)
print(out)
# [["a","a","b"],["aa","b"]]





