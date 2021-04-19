"""
    单路径，也就是说如果有两条最大，只给出一条。
"""
string_1 = 'abcdaf'
string_2 = 'zbcdf'
# string_1 = 'zzazazaz'
# string_2 = 'zzaazzaz'
length_1 = len(string_1)
length_2 = len(string_2)

dp = [[0 for _ in range(length_1 + 1)]]

for j in range(length_2):
    temp = [0]
    for i in range(length_1):
        temp.append(None)
    dp.append(temp)

use = [[False for j in range(length_1 + 1)] for i in range(length_2 + 1)]
pre = [[[None, None] for j in range(length_1 + 1)] for i in range(length_2 + 1)]

max_ = 0
max_index = None
for j in range(1, length_2 + 1):
    for i in range(1, length_1 + 1):
        if string_1[i - 1] == string_2[j - 1]:
            # dp[j][i] = max(dp[j-1][:i]) + 1
            # use[j][i] = True
            max_i = dp[j - 1][:i].index(max(dp[j - 1][:i]))
            dp[j][i] = dp[j - 1][max_i] + 1
            use[j][i] = True
            pre[j][i][0], pre[j][i][1] = j - 1, max_i
        else:
            # dp[j][i] = max(dp[j-1][:i])
            max_i = dp[j - 1][:i].index(max(dp[j - 1][:i]))
            dp[j][i] = dp[j - 1][max_i]
            pre[j][i][0], pre[j][i][1] = j - 1, max_i
        if dp[j][i] > max_:
            max_ = dp[j][i]
            max_index = [j, i]
print(max_)
print(max_index)
print(use)
print(pre)

max_str = ''
pre_char = max_index
count = 0
while True:
    if use[pre_char[0]][pre_char[1]]:
        max_str += string_2[pre_char[0] - 1]
        count += 1
    pre_char = pre[pre_char[0]][pre_char[1]]
    if count == max_:
        break

max_str = max_str[::-1]
print(max_str)
