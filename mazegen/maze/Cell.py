"""
Maze cell representation.

This module defines the Cell class, which models a single cell in the maze
grid.  Each cell tracks its four walls (N, E, S, W) and a visited flag used
during maze generation.
"""


class Cell():
    """
    A single cell in the maze grid.

    Each cell has four walls (North, East, South, West), represented as
    integers (1 = wall present, 0 = wall absent), and a boolean visited flag
    used by generation algorithms.
    """

    def __init__(self) -> None:
        """
        Initialize a cell with all walls intact and unvisited.
        """
        self._walls = {'N': 1,
                       'E': 1,
                       'S': 1,
                       'W': 1}
        self._visited = False

    def break_wall(self, direction: str) -> None:
        """
        Remove the wall on the given side of this cell.

        Args:
            direction (str): One of ``'N'``, ``'E'``, ``'S'``, or ``'W'``.
        """
        self._walls.update({direction: 0})

    def visited(self) -> None:
        """
        Mark this cell as visited.
        """
        self._visited = True

    def reset(self) -> None:
        """
        Reset the visited flag so the cell can be traversed again.
        """
        self._visited = False

    def get_hex(self) -> str:
        """
        Return a single hexadecimal character encoding the cell's wall state.

        Each wall direction is assigned a bit weight (N=1, E=2, S=4, W=8).
        The sum of the weights of present walls (value 1) is used as an index
        into the hexadecimal character set.

        Returns:
            str: A single character from ``'0123456789ABCDEF'``.
        """
        bit_weights = {'N': 1,
                       'E': 2,
                       'S': 4,
                       'W': 8}
        total = sum([self._walls[key] * value
                     for key, value in bit_weights.items()])
        return '0123456789ABCDEF'[total]

    def get_path(self) -> list[str]:
        """
        Return the directions in which this cell has open passages.

        Returns:
            list[str]: List of direction strings (``'N'``, ``'E'``, ``'S'``,
                ``'W'``) where the corresponding wall value is 0.
        """
        return [key for key in self._walls.keys()
                if self._walls[key] == 0]

    def close_block(self) -> bool:
        """
        Check whether all walls of this cell are intact (no open passages).

        Returns:
            bool: True if every wall is present (value 1), False if at least
                one wall has been removed.
        """
        if 0 in self._walls.values():
            return False
        return True

    def valid_cell(self) -> bool:
        """
        Check whether this cell is a valid carving target.

        A cell is considered valid when more than one of its walls is still
        intact, meaning it has not yet been fully carved into a dead-end
        during generation.

        Returns:
            bool: True if more than one wall is present, False otherwise.
        """
        walls = list(self._walls.values())
        return walls.count(1) >= 2
