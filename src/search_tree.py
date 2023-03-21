from __future__ import annotations

import functools
from queue import PriorityQueue

from .data_structures import Node
from .heuristics import Heuristic


class SearchTree:
    def __init__(self, initial_state: Node, heuristic: Heuristic):
        self._heuristic = heuristic
        estimate = self._heuristic.calculate(initial_state)
        self._root = STNode(initial_state, 0, estimate)
        self._frontier = PriorityQueue()
        self._frontier.put(self._root)

    def get_root(self):
        return self._root

    def get_heuristic(self):
        return self._heuristic

    def search(self, algorithm) -> int:
        return algorithm.calculate(self)


@functools.total_ordering
class STNode:  # Search Tree Node
    def __init__(self, state: Node, cost: int, estimate: int):
        self._cost = cost
        self._estimate = estimate
        self._state = state
        self._children = set()

    def get_estimate(self):
        return self._estimate

    def get_cost(self):
        return self._cost

    def add_child(self, child: STNode):
        self._children.add(child)

    def is_solution(self) -> bool:
        return self._state.is_solution()

    def __lt__(self, other: STNode):
        return (self._cost + self._estimate) < (other._cost + other._estimate)

    # TODO: implement in State
    def __eq__(self, other: STNode):
        return isinstance(other, STNode) and self._state == other._state

    def __hash__(self):
        return hash(self._state)
