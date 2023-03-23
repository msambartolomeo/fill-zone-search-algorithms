from abc import ABC

from src.state import State


class Heuristic(ABC):
    @staticmethod
    def calculate(state: State) -> int:
        pass


class DummyHeuristic(Heuristic):
    @staticmethod
    def calculate(state: State) -> int:
        return 0
