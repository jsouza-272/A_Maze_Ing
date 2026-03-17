from .Maze import Maze
from .Dfs import Dfs


class MazeGenerator():
    def __init__(self, width: int, height: int, entry: tuple[int],
                 exit: tuple[int], perfect: bool, seed: int = 42) -> None:
        self.maze = Maze(width, height)
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def generate_maze(self):
        algorithm = Dfs(self.seed)
        algorithm.generate_maze(self.maze, self.entry, exit)

    def show_maze(self):
        print(self.maze.get_hex_maze())
