from abc import ABC
from queue import PriorityQueue

from .search_tree import SearchTree


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


class GreedyAlgorithm(Algorithm):
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


class AStarAlgorithm(Algorithm):
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
