import json
import logging
import sys

import numpy as np

from src.algorithms import BfsAlgorithm, DfsAlgorithm, GreedyAlgorithm, AStarAlgorithm
from src.fill_zone.heuristics import ColorCountHeuristic, EccentricityHeuristic, CombinationHeuristic, \
    NodeCountHeuristic
from src.fill_zone.state import FillZoneGraphState
from src.heuristics import DummyHeuristic
from src.result import Result
from src.search_tree import SearchTree
from src.state import State


def get_algorithm(search_settings):
    match search_settings["algorithm"]:
        case "bfs":
            return BfsAlgorithm()
        case "dfs":
            return DfsAlgorithm()
        case "greedy":
            return GreedyAlgorithm()
        case "A*":
            return AStarAlgorithm()
        case _:
            raise ValueError("Unsupported search algorithm")


def get_heuristic(search_settings):
    if "heuristic" not in search_settings:
        return DummyHeuristic()

    match search_settings["heuristic"]:
        case "eccentricity":
            return EccentricityHeuristic()
        case "color_count":
            return ColorCountHeuristic()
        case "combination":
            return CombinationHeuristic()
        case "node_count":
            return NodeCountHeuristic()
        case _:
            return DummyHeuristic()


def generate_board(board_settings):
    match board_settings["type"]:
        case "static":
            return np.mat(board_settings["board"]).tolist()
        case "random":
            n = board_settings["board_size"]
            m = board_settings["color_count"]
            return np.random.randint(0, m, (n, n))
        case _:
            raise ValueError("Unsupported board generation method")


def main():
    if len(sys.argv) < 2:
        print("Config file argument not found")
        exit(1)
    config_path = sys.argv[1]
    with open(config_path, "r") as f:
        config = json.load(f)
    logging.basicConfig(level=logging.getLevelName(config["logging_level"]))
    board_settings = config["board_settings"]

    a = generate_board(board_settings)
    g: State = FillZoneGraphState(a)

    search_settings = config["search_settings"]
    algorithm = get_algorithm(search_settings)
    heuristic = get_heuristic(search_settings)

    search_tree: SearchTree = SearchTree(g, heuristic)

    result: Result = search_tree.search(algorithm)

    print("expanded nodes: ", result.expanded_nodes)
    print("solution found: ", result.solution)
    print("cost of solution: ", result.cost)
    print("nodes on frontier: ", result.frontier_nodes)


if __name__ == "__main__":
    main()
