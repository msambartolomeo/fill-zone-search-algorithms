import json
import sys
import numpy as np
from src.data_structures import Graph
import logging

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Config file argument not found")
        exit(1)
    config_path = sys.argv[1]
    with open(config_path, "r") as f:
        config = json.load(f)
        logging.basicConfig(level=logging.getLevelName(config["logging_level"]))
        board_settings = config["board_settings"]
        match board_settings["type"]:
            case "static":
                A = np.mat(board_settings["board"]).tolist()
            case "random":
                n = board_settings["board_size"]
                m = board_settings["color_count"]
                # TODO: Generate matrix
                raise NotImplemented()

    G = Graph.matrix_to_graph(A)
