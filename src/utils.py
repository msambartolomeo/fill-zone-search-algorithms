from .algorithms import *
from .heuristics import *


def get_all_algorithms() -> List[Algorithm]:
    ans = [DfsAlgorithm(), GreedyAlgorithm(), AStarAlgorithm()]
    return ans


def get_all_heuristics() -> List[Heuristic]:
    ans = [DijkstraHeuristic(), ColorCountHeuristic()]
    return ans
