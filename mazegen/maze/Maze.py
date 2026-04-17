"""
Maze grid representation.

This module defines the Maze class, which manages the 2-D grid of Cell
objects and provides helpers for maze generation (unvisited neighbor lookup)
and pathfinding (open neighbor lookup and direction calculation).
"""
from mazegen.maze.Cell import Cell


class Maze():
    """
    2-D grid of Cell objects representing a maze.

    Args:
        width (int): Number of columns.
        height (int): Number of rows.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the maze and build the base grid.

        Args:
            width (int): Number of columns in the maze.
            height (int): Number of rows in the maze.
        """
        self.width = width
        self.heigth = height
        self.maze = self._create_base()

    def _create_base(self) -> list[list[Cell]]:
        """
        Build and return the initial grid of fresh Cell objects.

        Returns:
            list[list[Cell]]: A 2-D list (rows × columns) of new Cell
                instances, each with all walls intact.
        """
        return [[Cell() for x in range(0, self.width)]
                for y in range(0, self.heigth)]

    def get_hex_maze(self) -> str:
        """
        Serialize the maze to a multi-line hexadecimal string.

        Each cell is encoded as a single hex character (see
        ``Cell.get_hex``). Rows are separated by newlines.

        Returns:
            str: Hexadecimal representation of the entire maze grid.
        """
        hex_maze = ''
        for row in self.maze:
            for column in row:
                hex_maze += column.get_hex()
            hex_maze += '\n'
        return hex_maze

    def unvisited_neighbors(self, x: int, y: int) -> list[tuple]:
        """
        Return all in-bounds, unvisited neighbors of position (x, y).

        Considers the four cardinal neighbors (N, S, W, E) and filters out
        any that are out of bounds or already visited.

        Args:
            x (int): Column index of the current cell.
            y (int): Row index of the current cell.

        Returns:
            list[tuple[int, int]]: List of (x, y) coordinates for valid
                unvisited neighbors.
        """
        limit_y = self.heigth
        limit_x = self.width
        candidate_neighbors = [(x, y - 1), (x, y + 1),
                               (x - 1, y), (x + 1, y)]
        neighbors = [(nx, ny) for nx, ny in candidate_neighbors
                     if 0 <= ny < limit_y and 0 <= nx < limit_x
                     and not self.maze[ny][nx]._visited
                     and self.maze[ny][nx].valid_cell()]
        return neighbors

    def get_neighbors(self, x: int, y: int,
                      reject: set | None = None) -> list[tuple]:
        """
        Return the coordinates of cells reachable from
        (x, y) through open walls.

        Only directions where the wall has been removed (``Cell.get_path``) are
        considered. An optional ``reject`` set can be used to exclude already
        processed nodes (e.g., the closed set in A*).

        Args:
            x (int): Column index of the current cell.
            y (int): Row index of the current cell.
            reject (set | None): Optional set of coordinates to exclude from
                the result.

        Returns:
            list[tuple[int, int]]: Coordinates of reachable neighbors.
        """
        directions = {'N': (x, y - 1),
                      'E': (x + 1, y),
                      'S': (x, y + 1),
                      'W': (x - 1, y)}
        neighbors = self.maze[y][x].get_path()
        if reject is None:
            return [directions[neighbor] for neighbor in neighbors]
        return [directions[neighbor] for neighbor in neighbors
                if directions[neighbor] not in reject]

    def get_pos(self, cell: Cell) -> tuple[int, int]:
        """
        Find and return the (x, y) position of the given Cell in the maze.

        Args:
            cell (Cell): The Cell instance to locate.

        Returns:
            tuple[int, int]: The (x, y) coordinate of the cell.

        Raises:
            KeyError: If the cell is not found in the maze grid.
        """
        for y in range(0, self.heigth):
            for x in range(0, self.width):
                if cell is self.maze[y][x]:
                    return x, y
        raise KeyError('Error: cell not in maze')

    def reset_visited(self) -> None:
        """
        Reset the visited flag on every cell in the maze.

        This allows the maze to be traversed again by generation or
        pathfinding algorithms without creating a new grid.
        """
        for line in self.maze:
            for _ in line:
                _.reset()

    @staticmethod
    def direction(current: tuple[int, int], next: tuple[int, int]) -> str:
        """
        Compute the cardinal direction from one cell to an adjacent cell.

        Args:
            current (tuple[int, int]): Source coordinate (x, y).
            next (tuple[int, int]): Destination coordinate (x, y).

        Returns:
            str: One of ``'N'``, ``'E'``, ``'S'``, or ``'W'``.
        """
        cx, cy = current
        nx, ny = next
        direction = ''
        if cx > nx:
            direction = 'W'
        if cx < nx:
            direction = 'E'
        if cy > ny:
            direction = 'N'
        if cy < ny:
            direction = 'S'
        return direction
