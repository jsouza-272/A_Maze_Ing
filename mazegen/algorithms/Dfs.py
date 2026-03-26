"""
Depth-first search maze carving algorithm.

This module implements the iterative DFS-based maze carving algorithm used to
generate perfect or imperfect mazes by randomly removing walls between cells.
"""
from mazegen.maze import Maze
import random


class Dfs():
    """
    Iterative depth-first search maze carver.

    Uses a stack to perform an iterative DFS traversal of the maze grid,
    randomly choosing unvisited neighbors and breaking walls between cells
    to carve passages.

    Args:
        seed (int | None): Optional RNG seed for reproducible maze generation.
    """

    def __init__(self, seed: int | None = None):
        """
        Initialize the DFS carver with an optional RNG seed.

        Args:
            seed (int | None): Seed for ``random.Random``. Pass ``None`` for a
                non-deterministic random sequence.
        """
        self.seed = random.Random(seed)

    def generate_maze(self, maze: Maze,
                      entry: tuple[int, int], exit: tuple[int, int]) -> None:
        """
        Carve passages through the maze using iterative DFS.

        Starting from ``entry``, the algorithm marks cells as visited and
        randomly breaks walls between adjacent unvisited cells.  Traversal
        stops when the stack is exhausted or when the exit cell is reached.

        Args:
            maze (Maze): Maze instance whose cells will be carved.
            entry (tuple[int, int]): Starting coordinate (x, y).
            exit (tuple[int, int]): Target coordinate that halts the current
                branch when reached.
        """
        stack: list = [entry]
        candidates = maze.unvisited_neighbors(*stack[-1])
        while stack:
            cx, cy = stack[-1]
            maze.maze[cy][cx].visited()
            candidates = maze.unvisited_neighbors(cx, cy)
            if len(candidates) == 0 or (cx, cy) == exit:
                stack.pop()
            else:
                nx, ny = self.seed.choice(candidates)
                maze.maze[cy][cx].break_wall(maze.direction(
                    (cx, cy), (nx, ny)))
                maze.maze[ny][nx].break_wall(maze.direction(
                    (nx, ny), (cx, cy)))
                stack.append((nx, ny))
