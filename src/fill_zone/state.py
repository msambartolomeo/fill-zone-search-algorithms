import logging
from copy import deepcopy
from queue import Queue
from typing import Set, Tuple, List, Optional

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from src.fill_zone.action import FillZoneAction
from src.fill_zone.data_structures import Node
from src.state import State


class FillZoneGraphState(State):
    def __init__(self, matrix: List[List[int]]):
        root, graph = matrix_to_graph(matrix)

        self._graph = graph
        self._root = root

    def is_solution(self) -> bool:
        return self._graph.number_of_nodes() == 1

    def is_dead(self) -> bool:
        return False

    def get_possible_actions(self) -> Set[FillZoneAction]:
        actions = set()
        for n in self._graph.neighbors(self._root):
            assert isinstance(n, Node)
            actions.add(FillZoneAction(n.color))
        return actions

    def apply(self, action: FillZoneAction) -> State:
        new_state: FillZoneGraphState = deepcopy(self)

        for child in new_state._graph[new_state._root].copy():
            if child.color == action.get_color():
                for grandchild in new_state._graph[child].copy():
                    if new_state._root != grandchild:
                        new_state._graph.add_edge(grandchild, new_state._root)
                new_state._graph.remove_node(child)

        root_edges = new_state._graph[new_state._root]
        new_state._graph.remove_node(new_state._root)
        new_state._root.color = action.get_color()
        new_state._graph.add_node(new_state._root)
        for child in root_edges:
            new_state._graph.add_edge(child, new_state._root)

        nx.draw(new_state._graph, with_labels=True)
        plt.show()

        return new_state

    def _merge_to_root(self, child: Node):
        child_edges = self._graph[child]
        for n in child_edges:
            self._graph.remove_edge(n, child)
            if self._root != n:
                self._graph.add_edge(n, self)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def get_neighbors(self, node: Node):
        return self.graph[node]

    @property
    def root(self):
        return self._root

    @property
    def graph(self):
        return self._graph


dxy = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


def in_range(x, a, b) -> bool:
    return a <= x < b


def matrix_to_graph(matrix: List[List[int]]) -> Tuple[Node, nx.Graph]:
    logging.info(f"Parsing graph from matrix {matrix}")
    nodes: List[List[Optional[Node]]] = [[None] * len(matrix[0]) for row in matrix]
    node_id = 1
    g = nx.Graph()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if nodes[i][j] is not None:
                continue
            curr_color: int = matrix[i][j]
            curr_node: Node = Node(curr_color, node_id)
            node_id += 1
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

                    if matrix[new_pos[0]][new_pos[1]] == curr_color and nodes[new_pos[0]][new_pos[1]] is None:
                        q.put((new_pos[0], new_pos[1]))
                        nodes[new_pos[0]][new_pos[1]] = curr_node
                    elif matrix[new_pos[0]][new_pos[1]] != curr_color and nodes[new_pos[0]][new_pos[1]] is not None:
                        neighbor: Node = nodes[new_pos[0]][new_pos[1]]
                        g.add_edge(neighbor, curr_node)

    logging.info(f"{[[id(cell) for cell in row] for row in nodes]}")

    return nodes[0][0], g


if __name__ == "__main__":
    mat = np.mat("4,5,5,3;4,3,0,3;3,4,0,2;1,5,1,0").tolist()

    state = FillZoneGraphState(mat)

    state = state.apply(FillZoneAction(5))

    state = state.apply(FillZoneAction(3))

    state = state.apply(FillZoneAction(2))

    state = state.apply(FillZoneAction(0))

    state = state.apply(FillZoneAction(4))

    state = state.apply(FillZoneAction(5))

    state = state.apply(FillZoneAction(1))
