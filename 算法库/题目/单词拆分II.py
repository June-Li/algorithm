def wordBreak(s, wordDict):
    dp = [[False for _ in range(len(s))] for _ in range(len(s))]
    dp_spilt = [[False for _ in range(len(s))] for _ in range(len(s))]

    s_len = len(s)
    for i in range(s_len):
        for j in range(i + 1):
            if s[j:i + 1] in wordDict:
                dp[i][j] = True
                if j == 0:
                    dp_spilt[i][j] = True
                elif sum(dp_spilt[j - 1][:]) > 0:
                    dp_spilt[i][j] = True

    split_list = []

    def search_fun(end, temp_str):
        if end < 0:
            temp_str.reverse()
            split_list.append(' '.join(temp_str))
            temp_str.reverse()
            return temp_str

        for start, i in enumerate(dp_spilt[end]):
            if i:
                temp_str.append(s[start:end+1])
                temp_str = search_fun(start-1, temp_str)[:-1]
        return temp_str

    search_fun(s_len-1, [])

    return split_list


# s = "catsanddog"
# wordDict = ["cat", "cats", "and", "sand", "dog"]
s = "pineapplepenapple"
wordDict = ["apple", "pen", "applepen", "pine", "pineapple"]
out = wordBreak(s, wordDict)
print(out)
