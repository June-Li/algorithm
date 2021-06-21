"""
v0
"""
def long_str_v0(string):
    length = len(string)
    dp = []
    for i in range(length):
        temp = []
        for j in range(length):
            if i == j:
                temp.append(True)
            else:
                temp.append(None)
        dp.append(temp)
    # print(dp)

    max_ = 1
    for j in range(length):
        for i in range(length):
            if i >= j:
                break
            if string[i] != string[j]:
                dp[i][j] = False
            else:
                if abs(i-j) < 3:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i+1][j-1]
            if dp[i][j] and abs(i-j)+1 > max_:
                max_ = abs(i-j)+1
    return max_


"""
v1：
    和v0一样，但是重新归整了下i，j的顺序；
"""


def long_str_v1(s):
    dp_ = [[False for _ in range(len(s))] for _ in range(len(s))]
    dp_[0][0] = True
    max_len = 1
    # i表示行（区间右侧），j表示列（区间左侧）
    for i in range(len(dp_)):
        for j in range(i + 1):
            if i - j == 0:
                dp_[i][j] = True
            elif abs(i - j) == 1:
                if s[i] == s[j]:
                    dp_[i][j] = True
            else:
                if s[i] == s[j]:
                    dp_[i][j] = dp_[i - 1][j + 1]
            if dp_[i][j]:
                if abs(i-j+1) > max_len:
                    max_len = i-j+1

    return max_len

a = 'sdgadfafda'
# ll = long_str_v0(a)
ll = long_str_v1(a)
print(ll)


