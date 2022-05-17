class Node:
    def __init__(self, val, next):
        self.val = val
        self.next = next


def print_listnode(head):
    cur = head
    while cur:
        print(cur.val, end='    ')
        cur = cur.next
    print()


def make_listnode(n):
    node = Node(n, None)
    for i in range(n-1, 0, -1):
        node = Node(i, node)
    return node


def reverse_listnode_iteration(head):
    cur = head.next
    pre = head
    pre.next = None
    while cur:
        cur.next, pre, cur = pre, cur, cur.next
    return pre


def reverse_listnode_recursion_1(cur, pre):
    cur.next, pre, cur = pre, cur, cur.next
    if not cur:
        return pre
    head = reverse_listnode_recursion_1(cur, pre)
    return head


def reverse_listnode_recursion_2(head):
    def fun(cur, pre):
        cur.next, pre, cur = pre, cur, cur.next
        if not cur:
            return pre
        head = fun(cur, pre)
        return head
    cur = head.next
    pre = head
    pre.next = None
    return fun(cur, pre)


def reverse_listnode_recursion_3(head):
    if not head.next:
        return head
    new_head = reverse_listnode_recursion_3(head.next)
    head.next.next = head
    head.next = None
    return new_head


print('ori listnode: ')
head = make_listnode(5)
print_listnode(head)

print('method iteration 1: ')
head = reverse_listnode_iteration(head)
print_listnode(head)

print('method recursion 1:')
cur = head.next
pre = head
pre.next = None
head = reverse_listnode_recursion_1(cur, pre)
print_listnode(head)

print('method recursion 2:')
head = reverse_listnode_recursion_2(head)
print_listnode(head)

print('method recursion 3:')
head = reverse_listnode_recursion_3(head)
print_listnode(head)
