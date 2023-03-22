from __future__ import annotations

from abc import ABC
from typing import Set

from .action import Action


class State(ABC):

    def is_solution(self) -> bool:
        raise NotImplementedError()

    def is_dead(self) -> bool:
        raise NotImplementedError()

    def get_possible_actions(self) -> Set[Action]:  # TODO: Review Action class or enum
        raise NotImplementedError()

    def apply(self, action: Action) -> State:
        raise NotImplementedError()
