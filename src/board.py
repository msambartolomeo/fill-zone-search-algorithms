from __future__ import annotations

from copy import deepcopy
from typing import List, Tuple
from queue import Queue
from main import generate_fill_zone_board
from src.fill_zone.action import FillZoneAction

# TODO: move these methods to avoid code repetition
dxy = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


def in_range(x, a, b) -> bool:
    return a <= x < b


class Board:
    def __init__(self, matrix: List[List[int]]):
        self._matrix = matrix

    def __str__(self):
        ans = ""
        for row in self._matrix:
            ans += row.__str__()
            ans += '\n'
        return ans

    def change_color(self, color: int):
        original_color = self._matrix[0][0]
        if original_color == color:
            return
        visited: List[List[bool]] = [[False] * len(self._matrix[0]) for _ in self._matrix]
        q: Queue[Tuple[int, int]] = Queue()
        q.put((0, 0))

        while not q.empty():
            pos = q.get()
            i = pos[0]
            j = pos[1]
            if visited[i][j]:
                continue

            visited[i][j] = True
            if self._matrix[i][j] == original_color:
                self._matrix[i][j] = color
                for dpos in dxy:
                    if in_range(i + dpos[0], 0, len(self._matrix)) and in_range(j + dpos[1], 0, len(self._matrix[0])):
                        q.put((i + dpos[0], j + dpos[1]))

    def is_solved(self) -> bool:
        color = self._matrix[0][0]
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[0])):
                if self._matrix[i][j] != color:
                    return False
        return True

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def check_solution(self, sol: List[FillZoneAction]) -> bool:
        copy: Board = deepcopy(self)
        for a in sol:
            copy.change_color(a.get_color())
        return copy.is_solved()

    def get_matrix(self) -> List[List[int]]:
        return self._matrix

    @staticmethod
    def from_string(s: str) -> Board:
        m = generate_fill_zone_board(s)
        return Board(m)


