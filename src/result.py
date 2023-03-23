from typing import List

from src.action import Action


class Result:
    def __init__(self, cost: int, expanded_nodes: int, frontier_nodes: int, solution: List[Action]):
        self.cost = cost
        self.expanded_nodes = expanded_nodes
        self.frontier_nodes = frontier_nodes
        self.solution = solution

    @classmethod
    def empty(cls, expanded_nodes: int):
        return cls(0, expanded_nodes, 0, [])

    def is_empty(self):
        return len(self.solution) == 0
