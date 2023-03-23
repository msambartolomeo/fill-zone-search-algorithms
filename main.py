import json
import logging
import sys
from typing import Tuple, List

import numpy as np

from src.algorithms import BfsAlgorithm, DfsAlgorithm, GreedyAlgorithm, AStarAlgorithm
from src.fill_zone.heuristics import ColorCountHeuristic, EccentricityHeuristic, CombinationHeuristic, \
    NodeCountHeuristic
from src.fill_zone.state import FillZoneGraphState
from src.heuristics import DummyHeuristic
from src.result import Result
from src.search_tree import SearchTree
from src.state import State
from src.eight_puzzle.state import EightPuzzleMatrixState
from src.eight_puzzle.heuristics import OutOfPlaceHeuristic, ManhattanHeuristic


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


def get_fill_zone_heuristic(search_settings):
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


def get_eight_puzzle_heuristic(search_settings):
    if "heuristic" not in search_settings:
        return DummyHeuristic()

    match search_settings["heuristic"]:
        case "out_of_place":
            return OutOfPlaceHeuristic()
        case "manhattan":
            return ManhattanHeuristic()
        case _:
            return DummyHeuristic()


def generate_fill_zone_board(board_settings):
    match board_settings["type"]:
        case "static":
            return np.mat(board_settings["board"]).tolist()
        case "random":
            n = board_settings["board_size"]
            m = board_settings["color_count"]
            return np.random.randint(0, m, (n, n))
        case _:
            raise ValueError("Unsupported board generation method")


# TODO: support more board creation settings
def generate_eight_puzzle_board(board_settings) -> Tuple[List[List[int]], List[List[int]]]:
    return np.mat(board_settings["board"]).tolist(), np.mat(board_settings["goal"]).tolist()


def run_fill_zone(config):
    board_settings = config["board_settings"]

    a = generate_fill_zone_board(board_settings)
    g: State = FillZoneGraphState(a)

    search_settings = config["search_settings"]
    algorithm = get_algorithm(search_settings)
    heuristic = get_fill_zone_heuristic(search_settings)

    search_tree: SearchTree = SearchTree(g, heuristic)
    result: Result = search_tree.search(algorithm)

    print("expanded nodes: ", result.expanded_nodes)
    print("solution found: ", result.solution)
    print("cost of solution: ", result.cost)
    print("nodes on frontier: ", result.frontier_nodes)


def run_eight_puzzle(config):
    board_settings = config["board_settings"]
    boards = generate_eight_puzzle_board(board_settings)
    s: EightPuzzleMatrixState = EightPuzzleMatrixState(boards[0], boards[1])
    search_settings = config["search_settings"]
    heuristic = get_eight_puzzle_heuristic(search_settings)
    algorithm = get_algorithm(search_settings)

    search_tree: SearchTree = SearchTree(s, heuristic)
    result: Result = search_tree.search(algorithm)

    print("expanded nodes: ", result.expanded_nodes)
    print("solution found: ", result.solution)
    print("cost of solution: ", result.cost)
    print("nodes on frontier: ", result.frontier_nodes)


def main():
    if len(sys.argv) < 2:
        print("Config file argument not found")
        exit(1)
    config_path = sys.argv[1]
    with open(config_path, "r") as f:
        config = json.load(f)
    logging.basicConfig(level=logging.getLevelName(config["logging_level"]))

    match config["game"]:
        case "fill-zone":
            return run_fill_zone(config)
        case "8-puzzle":
            return run_eight_puzzle(config)
        case _:
            raise ValueError("Game type not supported")


if __name__ == "__main__":
    main()
