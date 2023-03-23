from __future__ import annotations

import functools
from copy import deepcopy
from typing import Set, Optional

from .action import Action
from .heuristics import Heuristic
from .result import Result
from .state import State


class SearchTree:
    def __init__(self, initial_state: State, heuristic: Heuristic, algorithm):
        self._heuristic = heuristic
        self._root = STNode(self, initial_state, 0, None, None, algorithm.is_iterative())
        self._algorithm = algorithm

    def get_root(self):
        return self._root

    def get_heuristic(self):
        return self._heuristic

    def search(self) -> Result:
        return self._algorithm.search(self)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


@functools.total_ordering
class STNode:  # Search Tree Node
    def __init__(self, search_tree: SearchTree, state: State, cost: int, parent: Optional[STNode],
                 action: Optional[Action], depth_in_eq: bool):
        self._parent = parent
        self._action = action
        self._search_tree = search_tree
        self._cost = cost
        self._estimate = search_tree.get_heuristic().calculate(state)
        self._state = state
        self._children = set()
        self._depth_in_eq = depth_in_eq

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
        if isinstance(other, STNode):
            if self._depth_in_eq and other._depth_in_eq:
                return self._state == other._state and self._cost == other._cost
            else:
                return self._state == other._state
        return False

    def __hash__(self):
        return hash(self._state)

    def __repr__(self):
        return str(self._state)

    def expand(self) -> Set[STNode]:
        actions: Set[Action] = self._state.get_possible_actions()
        new_nodes: Set[STNode] = set()
        for a in actions:
            new_state: State = self._state.apply(a)
            new_node: STNode = STNode(self._search_tree, new_state, self._cost + 1, self, a, self._depth_in_eq)
            self.add_child(new_node)
            new_nodes.add(new_node)
        return new_nodes

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
