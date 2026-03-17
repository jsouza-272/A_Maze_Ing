from MazeGenerator.Cell import Cell


class Maze():
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.heigth = height
        self.maze = self._create_base()

    def _create_base(self) -> list[list[Cell]]:
        return [[Cell() for x in range(0, self.width)]
                for y in range(0, self.heigth)]

    def get_hex_maze(self) -> str:
        hex_maze = ''
        for row in self.maze:
            for column in row:
                hex_maze += column.get_hex()
            hex_maze += '\n'
        return hex_maze

    def unvisited_neighbors(self, x: int, y: int) -> list[tuple]:
        limit_y = self.heigth
        limit_x = self.width
        candidate_neighbors = [(x, y - 1), (x, y + 1),
                               (x - 1, y), (x + 1, y)]
        neighbors = [(nx, ny) for nx, ny in candidate_neighbors
                     if 0 <= ny < limit_y and 0 <= nx < limit_x
                     and not self.maze[ny][nx]._visited]
        return neighbors

    def get_pos(self, cell: Cell) -> tuple[int]:
        for y in range(0, self.heigth):
            for x in range(0, self.width):
                if cell is self.maze[y][x]:
                    return x, y
        return -1, -1

    @staticmethod
    def direction(current: tuple[int, int], next: tuple[int, int]) -> str:
        cx, cy = current
        nx, ny = next
        if cx > nx:
            return 'W'
        if cx < nx:
            return 'E'
        if cy > ny:
            return 'N'
        if cy < ny:
            return 'S'
