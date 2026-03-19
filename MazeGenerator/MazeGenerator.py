from .Maze import Maze
from .Dfs import Dfs


class MazeGenerator():
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int],
                 perfect: bool, seed: int = 42) -> None:
        self.maze = Maze(width, height)
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def generate_maze(self) -> None:
        algorithm = Dfs(self.seed)
        algorithm.generate_maze(self.maze, self.entry, self.exit)

    def get_maze(self) -> str:
        return self.maze.get_hex_maze()

    def draw_maze(self):
        w = self.maze.width
        h = self.maze.heigth

        top = '+'
        for c in range(w):
            cell = self.maze.maze[0][c]
            if cell._walls['N']:
                top += "---+"
            else:
                top += "   +"
        print(top)

        for y in range(h):
            mid = ""
            bottom = '+'

            for x in range(w):
                cell = self.maze.maze[y][x]
                if cell._walls['W']:
                    mid += '|'
                else:
                    mid += ' '

                if cell._walls['S']:
                    bottom += "---+"
                else:
                    bottom += "   +"

            last = self.maze.maze[y][-1]
            if last._walls['E']:
                mid += '|'
            else:
                " "
            print(mid)
            print(bottom)
