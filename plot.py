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
from src.result import Result
from src.search_tree import SearchTree
from src.state import State

OUTPUT_DIR = "figs/"
TEST_COUNT = 100
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


def _get_alias(o: object):
    return o.__class__.__name__[:3]


class PlotSupplier(ABC):

    def __init__(self, out_name: str):
        self._out_name = out_name

    def plot(self):
        M = 5
        N = 5
        data = {}
        for algo in UNINFORMED_ALGOS:
            data[_get_alias(algo)] = []
        for algo in INFORMED_ALGOS:
            for heu in HEURISTICS:
                data[f"{_get_alias(algo)} with {_get_alias(heu)}"] = []

        for t in range(TEST_COUNT):
            b: List[List[int]] = np.random.randint(0, M, (N, N)).tolist()
            for algo in UNINFORMED_ALGOS:
                g: State = FillZoneGraphState(b)
                search_tree = SearchTree(g, DummyHeuristic())
                start_time = time.time()
                res: Result = search_tree.search(algo)
                end_time = time.time()
                data[_get_alias(algo)].append(res.frontier_nodes)
            for algo in INFORMED_ALGOS:
                for heu in HEURISTICS:
                    g: State = FillZoneGraphState(b)
                    search_tree = SearchTree(g, heu)
                    start_time = time.time()
                    res: Result = search_tree.search(algo)
                    end_time = time.time()
                    data[f"{_get_alias(algo)} with {_get_alias(heu)}"].append(res.frontier_nodes)

        algos = list(data.keys())
        x_pos = np.arange(len(algos))
        means = [np.mean(data[algo]) for algo in algos]
        stds = [np.std(data[algo]) for algo in algos]

        fig, ax = plt.subplots()
        ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.5, ecolor='black')
        ax.set_ylabel('Frontier nodes')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(algos, rotation='vertical')
        ax.set_title('Algorithm')
        ax.yaxis.grid(True)

        # plt.tight_layout()
        ax.figure.autofmt_xdate()
        plt.savefig(OUTPUT_DIR + self._out_name)
        plt.show()


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    PlotSupplier("frontier_nodes_plot").plot()
