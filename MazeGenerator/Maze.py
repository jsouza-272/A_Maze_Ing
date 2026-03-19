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

    def get_neighbors(self, x: int, y: int,
                      reject: set | None = None) -> list[tuple]:
        directions = {'N': (x, y - 1),
                      'E': (x + 1, y),
                      'S': (x, y + 1),
                      'W': (x - 1, y)}
        neighbors = self.maze[y][x].get_path()
        if reject is None:
            return [directions[neighbor] for neighbor in neighbors]
        return [directions[neighbor] for neighbor in neighbors
                if directions[neighbor] not in reject]

    def get_pos(self, cell: Cell) -> tuple[int, int] | None:
        for y in range(0, self.heigth):
            for x in range(0, self.width):
                if cell is self.maze[y][x]:
                    return x, y
        return None

    @staticmethod
    def direction(current: tuple[int, int], next: tuple[int, int]) -> str:
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
