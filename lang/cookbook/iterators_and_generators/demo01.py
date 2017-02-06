# a generator only runs in response to iteration
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield
        x += increment

for n in frange(0, 4, 0.5):
    print(n)

# Example of iterating over two sequences as one

from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

# Iterating over merged sorted iterables

import heapq
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in heapq.merge(a, b):
    print(c)

# Example of delegating iteration to an internal container

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)
    # Outputs: Node(1), Node(2)


# Example of an object implementing both forward and reversed iterators

class Countdown:
    def __init__(self, start):
        self.start = start

    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # Reverse iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1

c = Countdown(5)
print("Forward:")
for x in c:
    print(x)

print("Reverse:")
for x in reversed(c):
    print(x)
