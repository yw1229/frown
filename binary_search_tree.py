class BiTreeNode:
    def __init__(self, data):
        self.data = data
        self.left_child = None
        self.right_child = None


class BST:
    def __init__(self, li):
        self.root = None
        if li:
            for val in li:
                self.insert(val)

    def insert(self, key):
        if not self.root:
            self.root = BiTreeNode(key)
        else:
            p = self.root
            while p:
                if key < p.data:  # key要存储在左子树
                    if p.left_child:  # 如果左子树有节点,往左子树走,继续看
                        p = p.left_child
                    else:  # 如果左子树是空,就插入到左孩子的位置
                        p.left_child = BiTreeNode(key)
                        break
                elif key > p.data:
                    if p.right_child:
                        p = p.right_child
                    else:
                        p.right_child = BiTreeNode(key)
                        break
                else:
                    break

    def query(self, key):
        p = self.root
        while p:
            if key < p.data:
                p = p.left_child
            elif key > p.data:
                p = p.right_child
            else:
                return True
        return False

    def traverse(self):
        def in_order(root):
            if root:
                in_order(root.left_child)
                print (root.data, end='')
                in_order(root.right_child)

        in_order(self.root)


tree = BST([5, 4, 6, 8, 7, 1, 9, 2, 3])
tree.traverse()
print (tree.query(6))
# 中序遍历是升序排列
