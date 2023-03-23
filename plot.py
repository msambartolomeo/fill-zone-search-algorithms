import os.path
import time
from abc import ABC
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from src.algorithms import BfsAlgorithm, DfsAlgorithm, GreedyAlgorithm, AStarAlgorithm
from src.fill_zone.heuristics import EccentricityHeuristic, ColorCountHeuristic
from src.fill_zone.state import FillZoneGraphState
from src.heuristics import DummyHeuristic
from src.search_tree import SearchTree
from src.state import State

OUTPUT_DIR = "figs/"
TEST_COUNT = 10
UNINFORMED_ALGOS = [
    BfsAlgorithm(),
    DfsAlgorithm()
]
HEURISTICS = [
    EccentricityHeuristic(),
    ColorCountHeuristic()
]
INFORMED_ALGOS = [
    GreedyAlgorithm(),
    AStarAlgorithm()
]


class PlotSupplier(ABC):

    def __init__(self, out_name: str):
        self._out_name = out_name

    def plot(self):
        M = 5
        N = 5
        data = {}
        for algo in UNINFORMED_ALGOS:
            data[algo.__class__.__name__] = []
        for algo in INFORMED_ALGOS:
            for heu in HEURISTICS:
                data[f"{algo.__class__.__name__} with {heu.__class__.__name__}"] = []

        for t in range(TEST_COUNT):
            b: List[List[int]] = np.random.randint(0, M, (N, N)).tolist()
            for algo in UNINFORMED_ALGOS:
                g: State = FillZoneGraphState(b)
                search_tree = SearchTree(g, DummyHeuristic())
                start_time = time.time()
                search_tree.search(algo)
                end_time = time.time()
                data[algo.__class__.__name__].append(end_time - start_time)
            for algo in INFORMED_ALGOS:
                for heu in HEURISTICS:
                    g: State = FillZoneGraphState(b)
                    search_tree = SearchTree(g, heu)
                    start_time = time.time()
                    search_tree.search(algo)
                    end_time = time.time()
                    data[f"{algo.__class__.__name__} with {heu.__class__.__name__}"].append(end_time - start_time)

        fig, ax = plt.subplots()
        ax.boxplot(
            [
                data_list for data_list in data.values()
            ]
        )
        plt.savefig(OUTPUT_DIR + self._out_name)


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    PlotSupplier("time_chart").plot()