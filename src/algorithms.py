from abc import ABC


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
    def calculate(root: SearchTreeNode):
        pass


class BfsAlgorithm(Algorithm):
    @staticmethod
    def calculate(root: SearchTreeNode):
        expanded = 0
        queue = [root]

        while len(queue):
            node = queue.pop(0)
            print(node)

            if node.is_goal():
                return expanded

            # Expand node
            expanded += 1
            for child in node.expand():
                queue.append(child)


class DfsAlgorithm(Algorithm):
    @staticmethod
    def calculate(root: SearchTreeNode):
        expanded = 0
        stack = [root]

        while len(stack):
            node = stack.pop()
            print(node)

            if node.is_goal():
                return expanded

            # Expand node
            expanded += 1
            for child in node.expand():
                stack.append(child)


class Greedy(Algorithm):
    @staticmethod
    def calculate(root: SearchTreeNode):
        pass


class AStar(Algorithm):
    @staticmethod
    def calculate(root: SearchTreeNode):
        pass
