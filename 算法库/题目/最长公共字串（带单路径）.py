"""
    单路径，也就是说如果有两条最大，只给出一条。
"""

string_1 = 'abcdaf'
string_2 = 'zbcdf'
length_1 = len(string_1)
length_2 = len(string_2)

dp = [[0 for _ in range(length_1 + 1)]]

for j in range(length_2):
    temp = [0]
    for i in range(length_1):
        temp.append(None)
    dp.append(temp)

max_ = 0
max_index = None
for j in range(1, length_2 + 1):
    for i in range(1, length_1 + 1):
        if string_1[i - 1] == string_2[j - 1]:
            dp[j][i] = dp[j - 1][i - 1] + 1
        else:
            dp[j][i] = 0
        if dp[j][i] > max_:
            max_ = dp[j][i]
            max_index = [j - 1, i - 1]
print(max_)
print(max_index)
max_str = ''
for i in range(max_):
    max_str += string_2[max_index[0] - i]
max_str = max_str[::-1]
print(max_str)
