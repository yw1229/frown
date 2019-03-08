# class StackWithTwoQueues(object):
#
#     """
#     push()操作：
#     为了保证先进栈的元素一直在栈底，需要将两个队列交替使用，才能满足需求。
#     因此，想法是，我们只在空的那个队列上添加元素，然后把非空的那个队列中的元素全部追加到当前这个队列。
#     这样一来，我们又得到一个空的队列，供下一次添加元素。
#  pop()操作：
#     因为在添加元素时，我们已经按照进栈的先后顺序把后进栈的元素放在一个队列的头部，
#     所以出栈操作时，我们只需要找到那个非空的队列，并依次取出数据即可。
#     """
#     def __init__(self):
#         self._queue1 = []
#         self._queue2 = []
#
#     def push(self, x):
#         if len(self._queue1) == 0:
#             self._queue1.append(x)
#         elif len(self._queue2) == 0:
#             self._queue2.append(x)
#         if len(self._queue2) == 1 and len(self._queue1) >= 1:
#             while self._queue1:
#                 self._queue2.append(self._queue1.pop(0))
#         elif len(self._queue1) == 1 and len(self._queue2) > 1:
#             while self._queue2:
#                 self._queue1.append(self._queue2.pop(0))
#
#     def pop(self):
#         if self._queue1:
#             return self._queue1.pop(0)
#         elif self._queue2:
#             return self._queue2.pop(0)
#         else:
#             return None
#
#     def getStack(self):
#         print("queue1", self._queue1)
#         print("queue2", self._queue2)
#
#
# sta = StackWithTwoQueues()
# sta.push(1)
# sta.push(2)
# sta.pop()
# sta.getStack()
# 俩个队列实现一个栈
# class Stack:
#     def __init__(self):
#         self.queueA = []
#         self.queueB = []
#
#     def push(self, node):
#         self.queueA.append(node)
#
#     def pop(self):
#         if len(self.queueA) == 0:
#             return None
#         while len(self.queueA) != 1:
#             self.queueB.append(self.queueA.pop(0))
#             print(self.queueB)
#         self.queueA, self.queueB = self.queueB, self.queueA  # 交换是为了下一次的pop
#         return self.queueB.pop()
#
#     def getStack(self):
#         print(self.queueA)
#         print(self.queueB)
# sta = Stack()
# for i in range(5):
#     sta.push(i)
# for i in range(5):
#     print(sta.pop())
# 俩个栈实现一个队列

class Queue(object):
    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def push(self, node):
        self.stack1.append(node)

    def pop(self):
        if self.stack2 == []:
            if self.stack1 == []:
                return None
            else:
                for i in range(len(self.stack1)):
                    self.stack2.append(self.stack1.pop())
        return self.stack2.pop()
