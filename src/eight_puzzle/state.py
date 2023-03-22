from __future__ import annotations

from copy import deepcopy
from typing import Optional, List, Set, Tuple

from src.eight_puzzle.action import EightPuzzleAction
from src.state import State


class EightPuzzleMatrixState(State):
    _GOAL = [[1, 2, 3], [8, None, 4], [7, 6, 5]]

    def __init__(self, matrix: List[List[Optional[int]]]):
        if len(matrix) != 3 or len(matrix[0]) != 3:
            raise ValueError()

        self._state: List[List[Optional[int]]] = matrix

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

    def apply(self, action: EightPuzzleAction) -> EightPuzzleMatrixState:  # Should I return State or EightPuzzleMatrixState
        new_state: EightPuzzleMatrixState = deepcopy(self)
        none_pos = self._find_none()
        if none_pos is None:
            raise ValueError()
        other_pos = (none_pos[0] + action.value[0], none_pos[1] + action.value[1])
        new_state._state[none_pos[0]][none_pos[1]] = self._state[other_pos[0]][other_pos[1]]
        new_state._state[other_pos[0]][other_pos[1]] = None
        return new_state

    def _find_none(self) -> Optional[Tuple[int, int]]:
        for i in range(3):
            for j in range(3):
                if self._state[i][j] is None:
                    return i, j
        return None

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
