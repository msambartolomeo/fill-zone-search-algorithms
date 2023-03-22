import heapq
from collections import deque
from typing import Set

from src.fill_zone.state import FillZoneGraphState
from src.heuristics import Heuristic


class DijkstraHeuristic(Heuristic):
    # TODO: Check
    @staticmethod
    def calculate(state: FillZoneGraphState) -> int:
        distances = {state: 0}
        unvisited = [(0, state)]
        max_distance = 0

        while unvisited:
            (dist, current) = heapq.heappop(unvisited)

            if current in distances and dist > distances[current]:
                continue

            for neighbor in current.neighbors:
                new_distance = distances[current] + 1

                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(unvisited, (new_distance, neighbor))

                    if new_distance > max_distance:
                        max_distance = new_distance

        return max_distance


class ColorCountHeuristic(Heuristic):
    @staticmethod
    def calculate(state: FillZoneGraphState) -> int:
        colors: Set[int] = set()
        count: int = 0

        for n in state.graph.nodes():
            if n == state.root:
                continue
            if n.color not in colors:
                colors.add(n.color)
                count += 1

        return count
