import json
import sys
import os
from typing import List

import numpy as np

from src.board import Board
from src.utils import get_all_algorithms, get_all_heuristics
from src.search_tree import SearchTree
from src.data_structures import Node


def test_all(boards: List[Board]):
    for b in boards:
        for h in get_all_heuristics():
            st: SearchTree = SearchTree(Node.matrix_to_graph(b.get_matrix()), h)
            for a in get_all_algorithms():
                sol = st.search(a)[1]
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
    for s in config["boards"]:
        boards.append(Board(np.mat(s).tolist()))

    test_all(boards)


if __name__ == "__main__":
    test()
