import heapq
from collections import deque

from src.fill_zone.state import FillZoneGraphState
from src.heuristics import Heuristic


class DijkstraHeuristic(Heuristic):
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
        colors = set()
        count = 1

        visited = set()
        queue = deque([state.root])
        visited.add(state.root)
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
