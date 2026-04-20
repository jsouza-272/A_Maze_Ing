"""
Prim's algorithm maze carving algorithm.

This module implements a randomized version of Prim's algorithm used to
generate perfect mazes by randomly selecting frontier edges and removing
walls between cells.
"""
from mazegen.maze import Maze
from typing import Generator
import random


class Prim():
    """
    Randomized Prim's algorithm maze carver.

    Uses a frontier list to perform a randomized Prim's traversal of the maze
    grid. Starting from the entry cell, the algorithm repeatedly picks a random
    edge connecting a visited cell to an unvisited one, removes the wall
    between them, and extends the frontier until all reachable cells are
    visited.

    Args:
        seed (int | None): Optional RNG seed for reproducible maze generation.
    """

    def __init__(self, seed: int | None = None):
        """
        Initialize the Prim carver with an optional RNG seed.

        Args:
            seed (int | None): Seed for ``random.Random``. Pass ``None`` for a
                non-deterministic random sequence.
        """
        self.seed = random.Random(seed)

    def generate_maze(self, maze: Maze,
                      entry: tuple[int, int],
                      exit: tuple[int, int],
                      first: bool = True) -> Generator:
        """
        Carve passages through the maze using randomized Prim's algorithm.

        Starting from ``entry``, the algorithm marks the cell as visited and
        collects its unvisited neighbors as frontier edges.  On each iteration,
        a random frontier edge is selected; if the target cell is still
        unvisited, the wall between the two cells is removed and the new cell's
        unvisited neighbors are added to the frontier.

        Args:
            maze (Maze): Maze instance whose cells will be carved.
            entry (tuple[int, int]): Starting coordinate (x, y).
            exit (tuple[int, int]): Target coordinate (unused directly, kept
                for interface compatibility with other algorithm classes).
            first (bool): If True, carves walls unconditionally (first pass,
                perfect maze). If False, only carves walls between cells that
                are still valid carving targets (second pass, adds extra
                passages for imperfect mazes). Defaults to True.
        """
        maze.maze[entry[1]][entry[0]].visited()
        frontiers = [(entry, neighbor)
                     for neighbor in maze.unvisited_neighbors(*entry)]
        while frontiers:
            chosen1, chosen2 = self.seed.choice(frontiers)
            x1, y1 = chosen1
            x2, y2 = chosen2
            frontiers.remove((chosen1, chosen2))
            if not maze.maze[y2][x2]._visited:
                maze.maze[y2][x2].visited()
                frontiers.extend([(chosen2, neighbor) for neighbor in maze.
                                  unvisited_neighbors(*chosen2)])
                if first:
                    maze.maze[y1][x1].break_wall(
                        maze.direction(chosen1, chosen2))
                    maze.maze[y2][x2].break_wall(
                        maze.direction(chosen2, chosen1))
                else:
                    if (maze.maze[y2][x2].valid_cell()
                            and maze.maze[y1][x1].valid_cell()):
                        maze.maze[y1][x1].break_wall(
                            maze.direction(chosen1, chosen2))
                        maze.maze[y2][x2].break_wall(
                            maze.direction(chosen2, chosen1))
                yield maze, chosen2
