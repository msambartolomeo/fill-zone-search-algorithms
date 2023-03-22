from __future__ import annotations

import functools
from typing import Set, Optional

from .action import Action
from .heuristics import Heuristic
from .state import State


class SearchTree:
    def __init__(self, initial_state: State, heuristic: Heuristic):
        self._heuristic = heuristic
        self._root = STNode(self, initial_state, 0, None, None)

    def get_root(self):
        return self._root

    def get_heuristic(self):
        return self._heuristic

    def search(self, algorithm) -> int:
        return algorithm.search(self)


@functools.total_ordering
class STNode:  # Search Tree Node
    def __init__(self, search_tree: SearchTree, state: State, cost: int, parent: Optional[STNode],
                 action: Optional[Action]):
        self._parent = parent
        self._action = action
        self._search_tree = search_tree
        self._cost = cost
        self._estimate = search_tree.get_heuristic().calculate(state)
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

    def get_parent(self) -> STNode | None:
        return self._parent

    def get_action(self) -> Action | None:
        return self._action

    def __lt__(self, other: STNode):
        return (self._cost + self._estimate) < (other._cost + other._estimate)

    def __eq__(self, other: STNode):
        return isinstance(other, STNode) and self._state == other._state

    def __hash__(self):
        return hash(self._state)

    def __repr__(self):
        return str(self._state)

    def expand(self) -> Set[STNode]:
        actions: Set[Action] = self._state.get_possible_actions()
        new_nodes: Set[STNode] = set()
        for a in actions:
            new_state: State = self._state.apply(a)
            new_node: STNode = STNode(self._search_tree, new_state, self._cost + 1, self, a)
            self.add_child(new_node)
            new_nodes.add(new_node)
        return new_nodes
