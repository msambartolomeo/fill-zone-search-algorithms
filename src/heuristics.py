from abc import ABC
from copy import deepcopy

from src.state import State


class Heuristic(ABC):
    @staticmethod
    def calculate(state: State) -> int:
        pass

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class DummyHeuristic(Heuristic):
    @staticmethod
    def calculate(state: State) -> int:
        return 0
