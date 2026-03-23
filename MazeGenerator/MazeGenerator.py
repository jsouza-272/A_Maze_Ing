from .maze.Maze import Maze
from .algorithms.Dfs import Dfs
from .Errors import FtError


class MazeGenerator():
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], output_file: str,
                 perfect: bool, seed: int = 42) -> None:
        self.maze = Maze(width, height)
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed

    def generate_maze(self) -> None:
        try:
            self.do_ft()
        except FtError as e:
            print(e)
        algorithm = Dfs(self.seed)
        algorithm.generate_maze(self.maze, self.entry, self.exit)
        if not self.perfect:
            self.maze.reset_visited()
            try:
                self.do_ft()
            except FtError:
                pass
            algorithm.generate_maze(self.maze, self.entry, self.exit)

    def do_ft(self) -> None:
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
                if self.exit == (w, h):
                    raise FtError('Error: exit point in "42" patern')
                if self.entry == (w + sx, h + sy):
                    raise FtError('Error: entry point in "42" patern')
                if bitmap[h][w] == '#':
                    self.maze.maze[sy + h][sx + w].visited()

    def get_maze(self) -> str:
        return self.maze.get_hex_maze()

    def save_maze(self) -> None:
        with open(self.output_file, 'w') as file:
            file.write(self.get_maze())
