from abc import ABC
from queue import PriorityQueue

from .search_tree import SearchTree


class SearchTreeNode:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.neighbours = set()

    def expand(self):
        raise NotImplemented()

    def is_goal(self):
        raise NotImplemented()


class Algorithm(ABC):
    @staticmethod
    def calculate(tree: SearchTree):
        pass


class BfsAlgorithm(Algorithm):
    @staticmethod
    def calculate(tree: SearchTree):
        expanded = 0
        queue = [tree.get_root()]

        while len(queue):
            node = queue.pop(0)
            print(node)

            if node.is_solution():
                return expanded

            # Expand node
            expanded += 1
            for child in node.expand():
                queue.append(child)


class DfsAlgorithm(Algorithm):
    @staticmethod
    def calculate(tree: SearchTree):
        expanded = 0
        stack = [tree.get_root()]

        while len(stack):
            node = stack.pop()
            print(node)

            if node.is_solution():
                return expanded

            # Expand node
            expanded += 1
            for child in node.expand():
                stack.append(child)


class Greedy(Algorithm):
    @staticmethod
    def calculate(tree: SearchTree):
        expanded = 0
        queue = PriorityQueue()
        root = tree.get_root()
        # Order in base to the cost
        queue.put((root.get_cost(), root))

        while not queue.empty():
            node = queue.get()
            print(node)

            if node.is_solution():
                return expanded

            # Expand node
            expanded += 1
            for child in node.expand():
                queue.put((child.get_cost(), child))
        pass


class AStar(Algorithm):
    @staticmethod
    def calculate(tree: SearchTree):
        expanded = 0
        queue = PriorityQueue()
        root = tree.get_root()
        # Order in base to the cost
        queue.put(root)

        while not queue.empty():
            node = queue.get()
            print(node)

            if node.is_solution():
                return expanded

            # Expand node
            expanded += 1
            for child in node.expand():
                queue.put(child)
        pass
