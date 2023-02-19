from collections import deque
from itertools import count
from heapq import heappush, heappop
from typing import Any


class CommonQueue:
    """Common class for Queue methods like iter and len."""

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        """Make the class usable in a for loop."""
        while len(self) > 0:
            yield self.dequeue()


class Queue(CommonQueue):
    """Implementation of FIFO queue"""

    def __init__(self, elements_args):
        self.elements = deque(elements_args)

    def dequeue(self):
        """Avoiding pop(0) in order not to be in O(n) time complexity."""
        return self.elements.popleft()

    def enqueue(self, elements):
        self.elements.append(elements)


class Stack(Queue):
    """Implementation of LIFO stack."""

    def dequeue(self):
        return self.elements.pop()


class PriorityQueue(CommonQueue):
    """Priority list which avoid O(n) time complexity like a list that should be sorted each time."""

    def __init__(self):
        self.elements = []
        self._counter = count()

    def enqueue_priority(self, priority: int, value: Any):
        """
        Insert to queue a value with a priority.
        The inserted element should contain tuple of priority integer (the bigger is high priority),
        and unique number (ot counter) to avoid alphabetical comparison between values with the same priority.
        :param priority: integer value of priority.
        :param value: The value.
        :return:
        """
        el = (priority, next(self._counter), value)
        heappush(self.elements, el)

    def dequeue(self):
        return heappop(self.elements)[-1]
