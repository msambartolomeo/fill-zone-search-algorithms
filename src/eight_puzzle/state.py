from __future__ import annotations

from typing import Optional, List, Set

from .action import EightPuzzleAction
from ..state import State


class EightPuzzleMatrixState(State):

    _GOAL = [[1, 2, 3], [8, None, 4], [7, 6, 5]]

    def __init__(self, matrix: List[List[Optional[int]]]):
        if len(matrix) != 3 or len(matrix[0]) != 3:
            raise ValueError()

        self._state: List[List[Optional[int]]] = [[], [], []]

    def is_solution(self) -> bool:
        return self._state == self._GOAL

    def is_dead(self) -> bool:
        return False

    def get_possible_actions(self) -> Set[EightPuzzleAction]:
        actions: Set[EightPuzzleAction] = set()
        if None not in self._state[0]:
            actions.add(EightPuzzleAction.UP)
        if None not in self._state[2]:
            actions.add(EightPuzzleAction.DOWN)
        if None not in [row[0] for row in self._state]:
            actions.add(EightPuzzleAction.LEFT)
        if None not in [row[2] for row in self._state]:
            actions.add(EightPuzzleAction.RIGHT)
        return actions
