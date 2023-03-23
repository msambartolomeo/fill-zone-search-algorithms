from enum import Enum

from src.action import Action


class EightPuzzleAction(Action, Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __repr__(self):
        match self:
            case EightPuzzleAction.UP:
                return "Up"
            case EightPuzzleAction.DOWN:
                return "Down"
            case EightPuzzleAction.LEFT:
                return "Left"
            case EightPuzzleAction.RIGHT:
                return "Right"
