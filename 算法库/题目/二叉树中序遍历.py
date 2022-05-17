# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def list_to_binarytree(nums):
    def level(index):
        if index >= len(nums) or nums[index] is None:
            return None, index

        root = TreeNode(nums[index])
        root.left, index = level(index + 1)
        root.right, index = level(index + 1)
        return root, index

    return level(0)[0]


# def list_to_binarytree(nums):
#     def level(index):
#         if index >= len(nums) or nums[index] is None:
#             return None
#
#         root = TreeNode(nums[index])
#         root.left, index = level(2*index + 1)
#         root.right, index = level(2*index + 2)
#         return root
#
#     return level(0)


"""
递归
"""
# def fun(root):
#     def recursive_search(root_, res_):
#         if not root_:
#             return
#         recursive_search(root_.left, res_)
#         res_.append(root_.val)
#         recursive_search(root_.right, res_)
#     res = []
#     recursive_search(root, res)
#     return res


"""
迭代
"""
def fun(root):
    res = []
    stk = []
    while root is not None or len(stk) > 0:
        while root is not None:
            stk.append(root)
            root = root.left
        root = stk[-1]
        stk.pop()
        res.append(root.val)
        root = root.right

    return res


example = {
    0: [[1, None, 2, 3], [1, 3, 2]],
    1: [[], []],
    2: [[1], [1]],
    3: [[1, 2], [2, 1]],
    4: [[1, None, 2], [1, 2]]
}
for key in example:
    root = list_to_binarytree(example[key][0])
    out = fun(root)
    print('实例: ', example[key][0])
    print('输出: ', out)
    print('预期: ', example[key][1], '\n')
