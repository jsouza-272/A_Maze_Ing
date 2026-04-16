"""
Maze generation pipeline.

This module defines the MazeGenerator class, which coordinates:
- maze structure creation
- optional placement of a "42" pattern obstacle (when the maze is large enough)
- generation of a perfect or imperfect maze using DFS-based carving
- serialization of the maze and entry/exit positions to an output file
"""
from .maze import Maze
from .algorithms import Dfs
from .algorithms import Prim
from .Errors import FtError
from typing import Type
from Ui import Ui
from time import sleep
import os


class MazeGenerator():
    """
    High-level maze generator and serializer.

    This class wraps the maze object and applies algorithms to generate a maze
    based on the provided configuration.

    Args:
        width (int): Maze width (number of columns).
        height (int): Maze height (number of rows).
        entry (tuple[int, int]): Entry coordinate (x, y).
        exit (tuple[int, int]): Exit coordinate (x, y).
        output_file (str): File path where the maze will be saved.
        perfect (bool): If True, generates a perfect maze (single solution).
        seed (int | None): Optional RNG seed for deterministic generation.
    """

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], output_file: str,
                 perfect: bool, seed: int | None = None,
                 algorithm: Type[Dfs] | Type[Prim] = Prim) -> None:
        """
        Initialize a MazeGenerator with configuration values.

        See class docstring for argument details.
        """
        self.maze = Maze(width, height)
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.algorithm = algorithm(seed)

    def generate_maze(self) -> None | str:
        """
        Generate the maze using DFS-based carving.

        This method optionally applies the "42" pattern (if the maze is large
        enough) and then runs the DFS algorithm to carve passages.

        If ``perfect`` is False, it performs an additional pass to create an
        imperfect maze by resetting visited flags and re-running generation.

        Raises:
            FtError: If the maze is too small to place the "42" pattern
                (the error is caught and printed; generation continues).
        """
        message = None
        try:
            self.do_ft()
        except FtError as e:
            self.maze.reset_visited()
            message = e.args[0]
        algorithm = self.algorithm
        for n in algorithm.generate_maze(self.maze, self.entry, self.exit):
            os.system('clear')
            Ui(n, []).show_maze(self.entry, exit, (255, 255, 255))
            sleep(0.5)
        if not self.perfect:
            self.maze.reset_visited()
            try:
                self.do_ft()
            except FtError:
                pass
            algorithm.generate_maze(self.maze, self.entry, self.exit)
        return message

    def do_ft(self) -> None:
        """
        Stamp a "42" obstacle pattern onto the maze grid.

        This method selects a bitmap representation of "42" that fits the
        current maze dimensions, centers it, and marks the corresponding cells
        as visited so the DFS carver treats them as walls.

        Raises:
            FtError: If the maze is too small to fit any supported bitmap, or
                if the entry/exit point overlaps with the pattern area.
        """
        if 9 <= self.maze.width and 7 <= self.maze.heigth:
            bitmap = ['#.#.###',
                      '#.....#',
                      '###.###',
                      '..#.#..',
                      '..#.###']
        elif 8 <= self.maze.width and 6 <= self.maze.heigth:
            bitmap = ['#.#.##',
                      '###..#',
                      '..#.#.',
                      '..#.##']
        else:
            raise FtError('Error: maze too small')
        bitmap_h = len(bitmap)
        bitmap_w = len(bitmap[0])
        sy = int((self.maze.heigth - bitmap_h) / 2)
        sx = int((self.maze.width - bitmap_w) / 2)
        for h in range(0, bitmap_h):
            for w in range(0, bitmap_w):
                if self.exit == (sx + w, sy + h) and bitmap[h][w] == '#':
                    raise FtError('Error: exit point in "42" patern')
                if self.entry == (w + sx, h + sy) and bitmap[h][w] == '#':
                    raise FtError('Error: entry point in "42" patern')
                if bitmap[h][w] == '#':
                    self.maze.maze[sy + h][sx + w].visited()

    def get_maze(self) -> str:
        """
        Return the maze serialized as a hexadecimal string.

        Returns:
            str: Hexadecimal representation of the maze produced by
                ``Maze.get_hex_maze``.
        """
        return self.maze.get_hex_maze()

    def save_maze(self) -> None:
        """
        Write the maze, entry, and exit coordinates to the output file.

        The file is written with three sections separated by newlines:
        1. The hexadecimal maze representation.
        2. The entry coordinate as ``x, y``.
        3. The exit coordinate as ``x, y``.
        """
        with open(self.output_file, 'w') as file:
            file.write(f'{self.get_maze()}\n')
            x, y = self.entry
            file.write(f'{x}, {y}\n')
            x, y = self.exit
            file.write(f'{x}, {y}\n')
