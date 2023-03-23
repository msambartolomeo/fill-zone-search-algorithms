import json
import sys
import os
from typing import List


from src.board import Board
from src.utils import get_all_algorithms, get_all_fill_zone_heuristics
from src.search_tree import SearchTree
from src.fill_zone.state import FillZoneGraphState
from main import generate_fill_zone_board


def test_all(boards: List[Board]):
    for b in boards:
        for h in get_all_fill_zone_heuristics():
            st: SearchTree = SearchTree(FillZoneGraphState(b.get_matrix()), h)
            for a in get_all_algorithms():
                sol = st.search(a).solution
                print(len(sol))
                assert b.check_solution(sol)


def test():
    if len(sys.argv) < 2:
        print("Config file argument not found")
        exit(1)
    config_path = sys.argv[1]
    print(os.getcwd())
    with open(config_path, "r") as f:
        config = json.load(f)
    boards: List[Board] = []
    settings = {
        "color_count": config["color_count"],
        "board_size": config["board_size"],
        "type": "random"
    }
    for _ in range(config["board_count"]):
        b = Board(generate_fill_zone_board(settings))
        boards.append(b)

    test_all(boards)


if __name__ == "__main__":
    test()
