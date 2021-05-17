def numDecodings(s):
    pre = 0
    if s[0] == '0':
        return pre
    pre = 1
    for i in range(1, len(s)):
        if s[i-1] == '0':
            if s[i] == 0:
                return 0
        else:
            if s[i] != '0' and int(s[i-1:i+1]) <= 26:
                pre += 2
            elif s[i] == '0' and int(s[i-1:i+1]) > 26:
                return 0

    return pre-1


# s = '90'
# s = '204'
s = "226"
# s = '5642618'
print(numDecodings(s))
