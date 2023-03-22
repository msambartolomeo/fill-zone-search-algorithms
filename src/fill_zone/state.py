from copy import deepcopy
from typing import Set, List

import networkx as nx

from .action import FillZoneAction
from src.state import State
from src.data_structures import Node


class FillZoneGraphState(State):
    def __init__(self, graph: nx.Graph, root: Node):
        self._graph = graph
        self._root = root

    def is_solution(self) -> bool:
        return self._graph.number_of_nodes() == 1

    def is_dead(self) -> bool:
        return False

    def get_possible_actions(self) -> Set[FillZoneAction]:
        actions = set()
        for n in self._graph.neighbors(self._root):
            assert isinstance(n, Node)
            actions.add(FillZoneAction(n.color))
        return actions

    def apply(self, action: FillZoneAction) -> State:
        new_state: FillZoneGraphState = deepcopy(self)
        new_state._root.color = action.get_color()
        for n in new_state._root.neighbors.copy():
            if n.color == action.get_color():
                new_state._merge_to_root(n)
        return new_state

    def _merge_to_root(self, child: Node):
        for n in child.neighbors.copy():
            self._graph.remove_edge(n, child)
            if self._root != n:
                self._graph.add_edge(n, self)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
