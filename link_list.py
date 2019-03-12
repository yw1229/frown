class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


# 带空头结点的链表 可以存长度
# head = Node()
# a = Node(1)  # 头结点
# b = Node(2)
# c = Node(3)  # 尾节点
# head.next = a
# a.next = b
# b.next = c

class LinkList:
    def __init__(self, li):
        self.head = None
        self.tail = None

        self.create_linklist_head(li)

    def create_linklist_head(self, li):
        self.head = Node(0)

        for v in li:
            n = Node(v)
            n.next = self.head.next
            self.head.next = n
            self.head.data += 1
            # print(self.head.data)

    def travers_link_list(self):
        p = self.head.next
        while p:
            print(p.data)
            p = p.next

    def create_link_list_tail(self, li):
        self.head = Node(0)
        self.tail = self.head
        for v in li:
            p = Node(v)
            self.tail.next = p
            self.tail = p
            self.head.data += 1


lts = LinkList([1, 2, 8, 4, 5])
lts.travers_link_list()
