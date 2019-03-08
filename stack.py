# class Stack():
#     def __init__(self, size):
#         self.size = size
#         self.stack = []
#         self.top = -1
#
#     def push(self, x):
#
#         # 入栈之前检查栈是否已满
#         if self.isfull():
#             raise Exception("stack is full")
#         else:
#             self.stack.append(x)
#             self.top = self.top + 1
#
#     def pop(self):
#
#         # 出栈之前检查栈是否为空
#         if self.isempty():
#             raise Exception ("stack is empty")
#         else:
#             self.top = self.top - 1
#             self.stack.pop()
#
#     def isfull(self):
#         return self.top + 1 == self.size
#
#     def isempty(self):
#         return self.top == -1
#
#     def showStack(self):
#         print(self.stack)


# s = Stack(10)

class Stack(object):
    def __init__(self, size):
        self.size = size
        self.stack = []
        self.top = -1

    def push(self, x):
        # 入栈之前检查栈是否已满
        if self.is_full():
            raise Exception('Stack is full')
        else:
            self.stack.append(x)
            self.top += 1

    def pull(self):
        # 出栈之前检查栈是否为空
        if self.is_empty():
            raise Exception('stack is empty')
        else:
            self.stack.pop()
            self.top -= 1

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top + 1 == self.size

    def show_stack(self):
        print(self.stack)


"""
类中有top属性，用来指示栈的存储情况，
初始值为1，一旦插入一个元素，其值加1，
利用top的值乐意判定栈是空还是满。

"""
s = Stack(10)
s.push(1)
s.push(5)
s.push(9)
s.pull()
s.push(2)
s.show_stack()
