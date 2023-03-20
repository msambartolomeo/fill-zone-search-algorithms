from __future__ import annotations
from typing import List, Set, Optional, Tuple
from queue import Queue
import logging


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
        root = self
        for n in self.neighbors.copy():
            if n.color == color:
                root = self._merge(n)
        return root

    def print_tree(self, visited=None):
        if visited is None:
            visited = set()
        visited.add(self)
        print(self)
        for n in self.neighbors:
            if n not in visited:
                n.print_tree(visited)


dxy = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


class Graph:
    def __init__(self, root: Node):
        self.root = root

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
                        new_pos = curr_pos + dpos
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
