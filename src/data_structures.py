from __future__ import annotations

from copy import copy, deepcopy
from typing import List, Set, Optional, Tuple
from queue import Queue
import logging

dxy = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


def in_range(x, a, b) -> bool:
    return a <= x < b


class Node:

    def __init__(self, color):
        self.color = color
        self._neighbors = set()

    def add_neighbor(self, n: Node):
        self._neighbors.add(n)
        n._neighbors.add(self)

    def remove_neighbor(self, n: Node):
        self._neighbors.remove(n)
        n._neighbors.remove(self)

    @property
    def neighbors(self) -> Set[Node]:
        return self._neighbors

    def is_solution(self) -> bool:
        return len(self._neighbors) == 0

    def __str__(self):
        return f"Color#{self.color}, neighbors={[n.color for n in self.neighbors]}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other: Node):
        return self.color < other.color

    @neighbors.setter
    def neighbors(self, value):
        self._neighbors = value

    def _merge(self, child: Node) -> Node:
        if child not in self.neighbors:
            raise ValueError()
        self.color = child.color
        for n in child.neighbors.copy():
            n.remove_neighbor(child)

            if self != n:
                self.add_neighbor(n)
        return self

    def change_color(self, color: int) -> Node:
        root = deepcopy(self)
        for n in root.neighbors.copy():
            if n.color == color:
                root._merge(n)
        return root

    def available_colors(self) -> Set[int]:
        ans = set()
        for n in self.neighbors:
            ans.add(n.color)
        return ans

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def print_tree(self, visited=None):
        if visited is None:
            visited = set()
        visited.add(self)
        print(self)
        for n in self.neighbors:
            if n not in visited:
                n.print_tree(visited)

    @staticmethod
    def matrix_to_graph(matrix: List[List[int]]) -> Node:
        logging.info("Parsing graph from matrix")
        logging.debug(f"Matrix: {matrix}")
        nodes: List[List[Optional[Node]]] = [[None] * len(matrix[0]) for row in matrix]

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if nodes[i][j] is not None:
                    continue

                logging.debug(f"Analizing cell ({i}, {j})")
                curr_color: int = matrix[i][j]
                curr_node: Node = Node(curr_color)
                nodes[i][j] = curr_node

                q: Queue[Tuple[int, int]] = Queue(maxsize=0)
                q.put((i, j))
                while not q.empty():
                    curr_pos: Tuple[int, int] = q.get()
                    for dpos in dxy:
                        new_pos = (curr_pos[0] + dpos[0], curr_pos[1] + dpos[1])
                        if (not in_range(new_pos[0], 0, len(matrix))) \
                                or (not in_range(new_pos[1], 0, len(matrix[0]))):
                            continue

                        logging.debug(
                            f"Neighbours in {new_pos} as {curr_pos} + {dpos} in range ({0}, {len(matrix[0])}) which returns {in_range(new_pos[1], 0, len(matrix[0]))}")
                        if matrix[new_pos[0]][new_pos[1]] == curr_color and nodes[new_pos[0]][new_pos[1]] is None:
                            q.put((new_pos[0], new_pos[1]))
                            nodes[new_pos[0]][new_pos[1]] = curr_node
                        elif matrix[new_pos[0]][new_pos[1]] != curr_color and nodes[new_pos[0]][new_pos[1]] is not None:
                            neighbor: Node = nodes[new_pos[0]][new_pos[1]]
                            neighbor.add_neighbor(curr_node)

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(hash(nodes[i][j]), sep="")
            print("")

        return nodes[0][0]
