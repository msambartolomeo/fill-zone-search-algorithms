from abc import ABC
from typing import Set


class State(ABC):

    def is_solution(self) -> bool:
        raise NotImplementedError()

    def is_dead(self) -> bool:
        raise NotImplementedError()

    def get_possible_actions(self) -> Set[Action]:  # TODO: Review Action class or enum
        raise NotImplementedError()

    # transition model
    # cost function