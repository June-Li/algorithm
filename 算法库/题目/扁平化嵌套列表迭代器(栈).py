"""
https://leetcode-cn.com/problems/flatten-nested-list-iterator/
341. 扁平化嵌套列表迭代器
    给你一个嵌套的整型列表。请你设计一个迭代器，使其能够遍历这个整型列表中的所有整数。
    列表中的每一项或者为一个整数，或者是另一个列表。其中列表的元素也可能是整数或是其他列表。
示例 1:
    输入: [[1,1],2,[1,1]]
    输出: [1,1,2,1,1]
解释: 通过重复调用 next 直到 hasNext 返回 false，next 返回的元素的顺序应该是: [1,1,2,1,1]。



这个方法更加有挑战性，也是这个题最正确的解法。因为对于大部分情况，我们希望迭代器能够一边迭代一边获取当前的结果，而不是提前初始化好。
把递归方法 转 迭代方法，我们需要用到「栈」。
在递归方法中，我们在遍历时如果遇到一个嵌套的 子list，就立即处理该 子list，直到全部展开；
在迭代方法中，我们不需要全部展开，只需要把 当前list 的所有元素放入 list 中。
由于「栈」的先进后出的特性，我们需要逆序在栈里放入各个元素。
处理流程分为两步：
在构造函数中应该初始化，把当前列表的各个元素（不用摊平）逆序放入栈中。
在 hasNext() 方法中，访问（不弹出）栈顶元素，判断是否为 int：
如果是 int 那么说明有下一个元素，返回 true；然后 next() 就会被调用，把栈顶的 int 弹出；
如果是 list 需要把当前列表的各个元素（不用摊平）逆序放入栈中。
如果栈为空，那么说明原始的嵌套列表已经访问结束了，返回 false。
"""


class NestedIterator(object):

    def __init__(self, nestedList):
        self.stack = []
        for i in range(len(nestedList) - 1, -1, -1):
            self.stack.append(nestedList[i])

    def next(self):
        cur = self.stack.pop()
        return cur.getInteger()

    def hasNext(self):
        while self.stack:
            cur = self.stack[-1]
            if cur.isInteger():
                return True
            self.stack.pop()
            for i in range(len(cur.getList()) - 1, -1, -1):
                self.stack.append(cur.getList()[i])
        return False
