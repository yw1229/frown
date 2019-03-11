from collections import deque


class BiTreeNode:
    def __init__(self, data):
        self.data = data
        self.left_child = None
        self.right_child = None


A = BiTreeNode('A')
B = BiTreeNode('B')
C = BiTreeNode('C')
D = BiTreeNode('D')
E = BiTreeNode('E')
F = BiTreeNode('F')
G = BiTreeNode('G')

A.right_child = C
C.right_child = D
C.left_child = B
G.right_child = F
E.left_child = A
E.right_child = G

root = E


# 前序遍历
# def pre_order(root):
#     if root:
#         print (root.data,end='')
#         pre_order(root.left_child)
#         pre_order(root.right_child)
#
#
# pre_order(root)
# 中序遍历
# def in_order(root):
#     if root:
#         in_order(root.left_child)
#         print (root.data, end='')
#         in_order(root.right_child)
#
#
# in_order(root)
#
#
# 后序遍历
# def post_order(root):
#     if root:
#         post_order(root.left_child)
#
#         post_order(root.right_child)
#         print (root.data, end='')


# in_order(root)
# 层次遍历
def level_order(root):
    q = deque()
    q.append(root)
    while (len(q) > 0):
        x = q.popleft()
        print (x.data, end='')
        if x.left_child:
            q.append(x.left_child)
        if x.right_child:
            q.append(x.right_child)


level_order(root)
# 后序定根,中序分左右
# 前序定根,中序分左右