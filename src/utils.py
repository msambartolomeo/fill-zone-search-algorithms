from .algorithms import *
from .heuristics import *
from .fill_zone.heuristics import EccentricityHeuristic, ColorCountHeuristic


def get_all_algorithms() -> List[Algorithm]:
    ans = [DfsAlgorithm(), BfsAlgorithm(), AStarAlgorithm(), GreedyAlgorithm()]
    return ans


def get_all_fill_zone_heuristics() -> List[Heuristic]:
    ans = [EccentricityHeuristic(), ColorCountHeuristic]
    return ans
