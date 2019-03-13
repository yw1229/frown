class Queue(object):

    def __init__(self, size):
        self.size = size
        self.front = -1
        self.rear = -1
        self.queue = []

    def enqueue(self, ele):
        # 入队操作
        if self.is_full():
            raise Exception("queue is full")
        else:
            self.queue.append(ele)
            self.rear = self.rear + 1

    def dequeue(self):

        # 出队操作
        if self.is_empty():
            raise Exception("queue is empty")
        else:
            self.queue.pop(0)
            self.front = self.front + 1

    def is_full(self):
        return self.rear - self.front + 1 == self.size

    def is_empty(self):
        return self.front == self.rear

    def showQueue(self):
        print(self.queue)


q = Queue(2)
print(q.is_empty())
q.enqueue(1)
q.enqueue(2)
print(q.is_full())

