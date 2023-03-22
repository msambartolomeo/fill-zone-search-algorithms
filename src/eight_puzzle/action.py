from enum import Enum

from ..action import Action


class EightPuzzleAction(Action, Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
