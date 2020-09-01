#!/usr/bin/env python3


# implement using 2 stacks
class MyQueue(object):

    def __init__(self):
        self.put_stack = []
        self.pop_stack = []

    def peek(self):
        self._try_fill_pop_stack()
        if len(self.pop_stack) == 0:
            return None

        return self.pop_stack[-1]

    def pop(self):
        if len(self.pop_stack) > 0:
            return self.pop_stack.pop()

        self._try_fill_pop_stack()
        if len(self.pop_stack) == 0:
            return None
        return self.pop_stack.pop()

    def put(self, value):
        self.put_stack.append(value)

    def _try_fill_pop_stack(self):
        if len(self.pop_stack) == 0 and len(self.put_stack) > 0:
            while len(self.put_stack) > 0:
                self.pop_stack.append(
                    self.put_stack.pop()
                )


queue = MyQueue()
t = int(input())
for line in range(t):
    values = map(int, input().split())
    values = list(values)
    if values[0] == 1:
        queue.put(values[1])
    elif values[0] == 2:
        queue.pop()
    else:
        print(queue.peek())
