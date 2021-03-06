"""
    编写一个函数，输入是一个无符号整数（以二进制串的形式），返回其二进制表达式中数字位数为 '1' 的个数（也被称为汉明重量）。

    输入：00000000000000000000000000001011
    输出：3
    解释：输入的二进制串 00000000000000000000000000001011 中，共有三位为 '1'。
"""

"""
    方法1：n & (n−1)，其预算结果恰为把 nn 的二进制位中的最低位的 11 变为 00 之后的结果。
    方法2：当检查第 ii 位时，我们可以让n与2^i进行与运算，当且仅当n的第i位为1时，运算结果不为0，2^i可以用1 << i表示。
"""