"""
A* pathfinding algorithm for maze solving.

This module implements the A* search algorithm using Manhattan distance as the
heuristic function.  It operates on a Maze instance and returns a list of
coordinates representing the shortest path from entry to exit.
"""
from ..maze.Maze import Maze
from ..Errors import AstarError
from typing import Generator


class Astar():
    """
    A* pathfinding algorithm.

    Uses Manhattan distance as the heuristic to find the shortest path between
    two coordinates inside a Maze.
    """

    @staticmethod
    def manhattan(pos: tuple[int, int], goal: tuple[int, int]) -> int:
        """
        Compute the Manhattan distance between two grid positions.

        Args:
            pos (tuple[int, int]): Current position (x, y).
            goal (tuple[int, int]): Target position (x, y).

        Returns:
            int: Sum of absolute differences of x and y coordinates.
        """
        result = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        return result

    def algorithm(self, maze: Maze,
                  entry: tuple, exit: tuple) -> list[tuple] | Generator:
        """
        Run the A* search on the given maze.

        Args:
            maze (Maze): Maze instance to search through.
            entry (tuple[int, int]): Start coordinate (x, y).
            exit (tuple[int, int]): Goal coordinate (x, y).

        Returns:
            list[tuple[int, int]]: Ordered list of coordinates from entry to
                exit (exclusive of the exit node itself).

        Raises:
            AstarError: If no path exists between entry and exit.
        """
        g = 0
        h = self.manhattan(entry, exit)
        f_score = {entry: g + h}
        g_score = {entry: g}
        openset = {entry}
        closeset: set = set()
        came_from = {}
        current_node = min(f_score, key=lambda k: f_score[k])

        while openset:
            current_node = min(f_score, key=lambda k: f_score[k])
            x, y = current_node
            neighbors = maze.get_neighbors(x, y, closeset)

            for n in neighbors:
                if n not in openset:
                    openset.add(n)
                    g_score[n] = g_score[current_node] + 1
                    f_score[n] = g_score[n] + self.manhattan(n, exit)
                    came_from[n] = current_node

                elif n in g_score and g_score[current_node] + 1 < g_score[n]:
                    g_score[n] = g_score[current_node] + 1
                    f_score[n] = g_score[n] + self.manhattan(n, exit)
                    came_from[n] = current_node

            openset.discard(current_node)
            f_score.pop(current_node)
            closeset.add(current_node)

            if current_node == exit:
                return self.make_path(came_from, entry, exit)

            yield current_node

        raise AstarError("Error: path not exist")

    def make_path(self, came_from: dict[tuple, tuple],
                  entry: tuple, exit: tuple) -> list[tuple]:
        """
        Reconstruct the path from the came_from map.

        Traces backwards from ``exit`` through ``came_from`` until ``entry``
        is reached, then returns the intermediate coordinates in forward order
        (entry is excluded from the result).

        Args:
            came_from (dict[tuple, tuple]): Mapping of node to its predecessor.
            entry (tuple[int, int]): Start coordinate (x, y).
            exit (tuple[int, int]): Goal coordinate (x, y).

        Returns:
            list[tuple[int, int]]: Intermediate path coordinates from just
                after entry up to and including exit.
        """
        path = {}
        current = exit
        while True:
            path[current] = came_from[current]
            current = came_from[current]
            if current == entry:
                break
        list_path = list(path.values())
        list_path.pop()
        return list_path

    @staticmethod
    def make_cardinal_path(list_path: list[tuple],
                           exit: tuple[int, int]) -> str:
        """
        Convert a list of path coordinates into a cardinal-direction string.

        Each consecutive pair of coordinates is translated into a compass
        direction (N, E, S, W) using ``Maze.direction``.

        Args:
            list_path (list[tuple[int, int]]): Mutable list of path
                coordinates (will be consumed by this method).
            exit (tuple[int, int]): Final destination coordinate (x, y).

        Returns:
            str: String of cardinal direction characters representing the path.
        """
        cardinal_path = ''
        while list_path:
            xy = list_path.pop()
            if list_path:
                cardinal_path += Maze.direction(xy, list_path[-1])
            else:
                cardinal_path += Maze.direction(xy, exit)
        return cardinal_path
