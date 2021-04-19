def long_str(string):
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


a = 'bbaaaaaaaabb'
ll = long_str(a)
print(ll)
