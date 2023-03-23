from src.heuristics import Heuristic
from src.eight_puzzle.state import EightPuzzleMatrixState


class OutOfPlaceHeuristic(Heuristic):
    @staticmethod
    def calculate(state: EightPuzzleMatrixState) -> int:
        estimate = 0
        m = state.get_matrix()
        g = state.get_goal()
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j] is not None and m[i][j] != g[i][j]:
                    estimate += 1
        return estimate
