class Node(object):
    def __init__(self, value):
        # 元素域
        self.value = value
        # 链接域
        self.next = None


class CircularLinkedListOneway(object):
    def __init__(self, node=None):
        # 构造非空链时，让其地址域指向自己
        if node:
            node.next = node
        self.__head = node

    def is_empty(self):
        # 头节点不为None则不为空
        return self.__head == None

    def __len__(self):
        count = 1
        cur = self.__head
        if self.is_empty():
            return 0
        while cur.next != self.__head:
            count += 1
            cur = cur.next
        return count

    def traversal(self):
        if self.is_empty():
            return
        cur = self.__head
        while cur.next != self.__head:
            print(cur.value)
            cur = cur.next
        # 退出循环时，cur正是尾节点
        print(cur.value)

    def link_head(self):
        return self.__head

    def next_node(self, cur):
        if self.is_empty():
            return
        return cur.next

    def add(self, value):
        """头插法"""
        node = Node(value)
        if self.is_empty():
            self.__head = node
            self.__head.next = self.__head
            return
        cur = self.__head
        while cur.next != self.__head:
            cur = cur.next
        # 新节点的next指针指向原头节点
        node.next = self.__head
        # 将新节点指向头节点
        self.__head = node
        # 尾节点next指针指向新头节点
        cur.next = self.__head

    def append(self, value):
        node = Node(value)
        cur = self.__head
        if self.is_empty():
            self.__head = node
            self.__head.next = self.__head
            return
        while cur.next != self.__head:
            cur = cur.next
        node.next = cur.next
        cur.next = node

    def insert(self, pos, value):
        if pos <= 0:
            self.add(value)
        elif pos > len(self) - 1:
            self.append(value)
        else:
            node = Node(value)
            cur = self.__head
            count = 0
            while count < pos - 1:
                count += 1
                cur = cur.next
            node.next = cur.next
            cur.next = node

    def search(self, value):
        if self.is_empty():
            return False
        cur = self.__head
        while cur.next != self.__head:
            if cur.value == value:
                return True
            else:
                cur = cur.next
        # 别忘了while循环外的尾节点
        if cur.value == value:
            return True
        return False

    def remove(self, value):
        cur = self.__head
        prior = None
        if self.is_empty():
            return
        while cur.next != self.__head:
            # 待删除节点如果找到
            if cur.value == value:
                # 待删除节点在头部
                if cur == self.__head:
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next
                    self.__head = cur.next
                    rear.next = self.__head
                # 待删除节点在中间
                else:
                    prior.next = cur.next  # 这里不是跳出循环的break,而是退出函数的return哦,因为已经处理完毕了
                return
            # 如果还没找到
            else:
                prior = cur
                cur = cur.next
        # 待删除节点在尾部
        if cur.value == value:
            # 如果链表中只有一个元素，则此时prior为None，Next属性就会报错
            # 此时直接使其头部元素为None即可
            if cur == self.__head:
                self.__head = None
                return
            prior.next = cur.next


# # 将数字1 2 3 4 5 6从尾部插入链表
# scll = CircularLinkedListOneway()
# scll.append(1)
# scll.append(2)
# scll.append(3)
# scll.append(4)
# scll.append(5)
# scll.append(6)
# node = scll.link_head()
# for i in range(100):
#     node = scll.next_node(node)
#     print(node.value)
# scll.traversal()    # 遍历链表
