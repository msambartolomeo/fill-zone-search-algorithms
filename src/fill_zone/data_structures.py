from __future__ import annotations

from copy import deepcopy


class Node:

    def __init__(self, color, node_id):
        self._id = node_id
        self.color = color

    def __str__(self):
        return f"{self._id}. Color#{self.color}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other: Node):
        return self.color < other.color

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __eq__(self, other):
        return isinstance(other, Node) and self._id == other._id and self.color == other.color

    def __hash__(self):
        return hash((self._id, self.color))
