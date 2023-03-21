from __future__ import annotations

import functools
from typing import List
from .heuristics import Heuristic
from .data_structures import Node
from queue import PriorityQueue


class SearchTree:
    def __init__(self, initial_state: Node, heuristic: Heuristic):
        self._heuristic = heuristic
        estimate = self._heuristic.calculate(initial_state)
        self._root = STNode(initial_state, 0, estimate)
        self._frontier = PriorityQueue()
        self._frontier.put(self._root)

    def search(self) -> List[int]:
        while not self._frontier.empty():
            curr_node: STNode = self._frontier.get()
            if curr_node.is_solution():
                # Hooray!
                pass
            self._frontier.put(curr_node.expand())


@functools.total_ordering
class STNode:  # Search Tree Node
    def __init__(self, state: Node, cost: int, estimate: int):
        self._cost = cost
        self._estimate = estimate
        self._state = state
        self._children = set()

    def add_child(self, child: STNode):
        self._children.add(child)

    def is_solution(self) -> bool:
        return self._state.is_solution()

    def __lt__(self, other: STNode):
        return (self._cost + self._estimate) < (other._cost + other._estimate)
