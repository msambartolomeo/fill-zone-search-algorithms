import heapq
from abc import ABC
from collections import deque
from copy import deepcopy

from .data_structures import Node


class Heuristic(ABC):
    @staticmethod
    def calculate(state: Node) -> int:
        pass

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class DummyHeuristic(Heuristic):
    @staticmethod
    def calculate(state: Node) -> int:
        return 0


class DijkstraHeuristic(Heuristic):
    @staticmethod
    def calculate(state: Node) -> int:
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
    def calculate(state: Node) -> int:
        colors = set()
        count = 1

        visited = set()
        queue = deque([state])
        visited.add(state)
        colors.add(state.color)

        while queue:
            current = queue.popleft()

            for neighbor in current.neighbors:

                if neighbor not in visited:

                    visited.add(neighbor)
                    queue.append(neighbor)
                    if neighbor.color not in colors:
                        colors.add(neighbor.color)
                        count += 1
        return count
