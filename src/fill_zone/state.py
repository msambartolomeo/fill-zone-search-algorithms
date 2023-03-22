from copy import deepcopy
from typing import Set

from .action import FillZoneAction
from src.state import State
from src.data_structures import Node


class FillZoneState(State):

    def __init__(self, root: Node):
        self._root = root

    def is_solution(self) -> bool:
        return len(self._root.neighbors) == 0

    def is_dead(self) -> bool:
        return False

    def get_possible_actions(self) -> Set[FillZoneAction]:
        actions = set()
        for n in self._root.neighbors:
            actions.add(FillZoneAction(n.color))
        return actions

    def apply(self, action: FillZoneAction) -> State:
        new_state: FillZoneState = deepcopy(self)
        new_state._root.color = action.get_color()
        for n in new_state._root.neighbors.copy():
            if n.color == action:
                self._merge_to_root(n)
        return new_state

    def _merge_to_root(self, child: Node):
        for n in child.neighbors.copy():
            n.remove_neighbor(child)
            if self._root != n:
                self._root.add_neighbor(n)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
