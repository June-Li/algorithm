def romanToInt(s):
    all = 0
    roma_dict = {'I': [0, 1], 'V': [1, 5], 'X': [2, 10], 'L': [3, 50], 'C': [4, 100], 'D': [5, 500], 'M': [6, 1000],
                 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    skip = False
    for idx, i in enumerate(s):
        if skip:
            skip = False
            continue
        if idx+1 <= len(s)-1 and roma_dict[s[idx]][0] < roma_dict[s[idx+1]][0]:
            all += roma_dict[s[idx:idx + 2]]
            skip = True
        else:
            all += roma_dict[s[idx]][1]
            skip = False
    return all


# s = 'III'
# 输出: 3
# s = "IV"
# 输出: 4
# s = "IX"
# 输出: 9
# s = "LVIII"
# 输出: 58
s = "MCMXCIV"
# 输出: 1994

out = romanToInt(s)
print(out)
