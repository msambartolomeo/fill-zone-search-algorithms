from abc import ABC
from copy import deepcopy
from queue import PriorityQueue, Queue
from typing import List, Tuple, Set, Callable

from .action import Action
from .result import Result
from .search_tree import SearchTree, STNode


def get_solution(node: STNode) -> List[Action]:
    solution = [node.get_action()]
    parent = node.get_parent()

    while parent is not None:
        solution.append(parent.get_action())
        parent = parent.get_parent()

    solution.pop()
    solution.reverse()
    return solution


class Algorithm(ABC):
    def search(self, tree: SearchTree) -> Result:
        expanded = 0
        frontier = self._create_frontier()
        self._add_to_frontier(frontier, tree.get_root())
        visited: Set[STNode] = set()

        while not self._frontier_is_empty(frontier):
            curr_node = self._get_from_frontier(frontier)
            if curr_node in visited:
                continue

            visited.add(curr_node)

            if curr_node.is_solution():
                return Result(curr_node.get_cost(), expanded, self._frontier_length(frontier), get_solution(curr_node))

            # Expand node
            expanded += 1
            for child in curr_node.expand():
                self._add_to_frontier(frontier, child)

        return Result.empty(expanded)

    def is_iterative(self):
        return False

    def _create_frontier(self):
        raise NotImplementedError()

    def _add_to_frontier(self, frontier, node: STNode):
        raise NotImplementedError()

    def _get_from_frontier(self, frontier) -> STNode:
        raise NotImplementedError()

    def _frontier_is_empty(self, frontier) -> bool:
        raise NotImplementedError()

    def _frontier_length(self, frontier) -> int:
        raise NotImplementedError()


class BfsAlgorithm(Algorithm):
    def _create_frontier(self) -> Queue[STNode]:
        return Queue()

    def _add_to_frontier(self, frontier: Queue[STNode], node: STNode):
        frontier.put(node)

    def _get_from_frontier(self, frontier: Queue[STNode]) -> STNode:
        return frontier.get()

    def _frontier_is_empty(self, frontier: Queue[STNode]) -> bool:
        return frontier.empty()

    def _frontier_length(self, frontier: Queue[STNode]) -> int:
        return frontier.qsize()


class DfsAlgorithm(Algorithm):
    def _create_frontier(self) -> List[STNode]:
        return []

    def _add_to_frontier(self, frontier: List[STNode], node: STNode):
        frontier.append(node)

    def _get_from_frontier(self, frontier: List[STNode]) -> STNode:
        return frontier.pop()

    def _frontier_is_empty(self, frontier: List[STNode]) -> bool:
        return len(frontier) == 0

    def _frontier_length(self, frontier: List[STNode]) -> int:
        return len(frontier)


class GreedyAlgorithm(Algorithm):
    def _create_frontier(self) -> PriorityQueue[Tuple[int, STNode]]:
        return PriorityQueue()

    def _add_to_frontier(self, frontier: PriorityQueue[Tuple[int, STNode]], node: STNode):
        frontier.put((node.get_estimate(), node))

    def _get_from_frontier(self, frontier: PriorityQueue[Tuple[int, STNode]]) -> STNode:
        order, node = frontier.get()
        return node

    def _frontier_is_empty(self, frontier: PriorityQueue[Tuple[int, STNode]]) -> bool:
        return frontier.empty()

    def _frontier_length(self, frontier: PriorityQueue[Tuple[int, STNode]]) -> int:
        return frontier.qsize()


class AStarAlgorithm(Algorithm):
    def _create_frontier(self) -> PriorityQueue[Tuple[int, STNode]]:
        return PriorityQueue()

    def _add_to_frontier(self, frontier: PriorityQueue[Tuple[int, STNode]], node: STNode):
        frontier.put((node.get_estimate() + node.get_cost(), node))

    def _get_from_frontier(self, frontier: PriorityQueue[Tuple[int, STNode]]) -> STNode:
        order, node = frontier.get()
        return node

    def _frontier_is_empty(self, frontier: PriorityQueue[Tuple[int, STNode]]) -> bool:
        return frontier.empty()

    def _frontier_length(self, frontier: PriorityQueue[Tuple[int, STNode]]) -> int:
        return frontier.qsize()


class IDDFSAlgorithm(Algorithm):
    def search(self, tree: SearchTree) -> Result:
        test_tree = deepcopy(tree)
        expanded = 0

        while (result := super().search(test_tree)).is_empty():
            self._depth = self._update_depth(self._depth)
            test_tree = deepcopy(tree)
            expanded += result.expanded_nodes

        result.expanded_nodes += expanded

        return result

    def is_iterative(self):
        return True

    def __init__(self, depth: int, update_depth: Callable[[int], int]):
        self._depth = depth
        self._update_depth = update_depth

    def _create_frontier(self) -> List[STNode]:
        return []

    def _add_to_frontier(self, frontier: List[STNode], node: STNode):
        if node.get_cost() <= self._depth:
            frontier.append(node)

    def _get_from_frontier(self, frontier: List[STNode]) -> STNode:
        return frontier.pop()

    def _frontier_is_empty(self, frontier: List[STNode]) -> bool:
        return len(frontier) == 0

    def _frontier_length(self, frontier: List[STNode]) -> int:
        return len(frontier)
