"""
这是一道类似最大子串、最大子序列、最大回文子串；
优化：
    使用滚动数组，可以节省空间，因为dp只需要上一行，所以没必要全部保存；
"""
def isInterleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    dp = [[False for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]
    dp[0][0] = True
    for i in range(1, len(s1)+1):
        if dp[i-1][0] and s1[i-1] == s3[i-1]:
            dp[i][0] = True
    for i in range(1, len(s2)+1):
        if dp[0][i-1] and s2[i-1] == s3[i-1]:
            dp[0][i] = True
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]) or (dp[i-1][j] and s1[i - 1] == s3[i + j - 1]):
                dp[i][j] = True
    return dp[-1][-1]


s1 = "aabcc"
s2 = "dbbca"
s3 = "aadbbcbcac"
# s1 = 'aa'
# s2 = 'b'
# s3 = 'abb'
isInterleave(s1, s2, s3)
