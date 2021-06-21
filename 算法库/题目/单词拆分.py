def wordBreak(s, wordDict):
    dp = [[False for _ in range(len(s))] for _ in range(len(s))]
    dp_spilt = [[False for _ in range(len(s))] for _ in range(len(s))]
    s_len = len(s)
    for i in range(s_len):
        for j in range(i+1):
            if s[j:i+1] in wordDict:
                dp[i][j] = True
                if j == 0:
                    dp_spilt[i][j] = True
                elif dp_spilt[j-1][0] > 0:
                    dp_spilt[i][j] = True
        dp_spilt[i][:] = [sum(dp_spilt[i][:])]
    return bool(sum(dp_spilt[-1]))


s = "leetcode"
wordDict = ["leet", "code"]
# s = "applepenapple"
# wordDict = ["apple", "pen"]
out = wordBreak(s, wordDict)
print(out)
