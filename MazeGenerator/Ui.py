from .maze.Maze import Maze
import os


class Ui():
    def __init__(self, maze: Maze, path: list) -> None:
        self.maze = maze
        self.path = path

    def clean(self) -> None:
        os.system('clean')

    def show_maze(self, entry: tuple, exit: tuple, path: bool = False) -> None:
        if path:
            for line in self.render_path(entry, exit, (0, 255, 0)):
                for _ in line:
                    print(_, end='')
                print()
        else:
            for line in self.render(entry, exit):
                for _ in line:
                    print(_, end='')
                print()

    def render(self, entry: tuple, exit: tuple) -> list[list[str]]:
        render_maze = []
        w = self.maze.width
        h = self.maze.heigth
        maze = self.maze
        reset_collor = '\033[0m'
        white = '255;255;255'

        final_line = []

        for _ in range(0, w):
            final_line.append(f'\033[38;2;{white}m█████\033[0m')
        final_line.append(f'\033[38;2;{white}m█\033[0m')

        for y in range(0, h):
            line1 = []
            line2 = []

            for x in range(0, w):
                if maze.maze[y][x]._walls['N']:
                    line1.append(f'\033[38;2;{white}m█████\033[0m')
                else:
                    line1.append(f'\033[38;2;{white}m█\033[0m    ')

                if maze.maze[y][x]._walls['W']:
                    if maze.maze[y][x].close_block():
                        line2.append(f'\033[38;2;{white}m█\033[0m\
\033[48;2;100;100;100m    \033[0m')
                    elif (x, y) == entry:
                        line2.append(f'\033[38;2;{white}m█{reset_collor}\
\033[48;2;0;0;255m    {reset_collor}')
                    elif (x, y) == exit:
                        line2.append(f'\033[38;2;{white}m█{reset_collor}\
\033[48;2;255;0;0m    {reset_collor}')
                    else:
                        line2.append(f'\033[38;2;{white}m█\033[0m    ')
                else:
                    if (x, y) == entry:
                        line2.append(f' \033[48;2;0;0;255m    {reset_collor}')
                    elif (x, y) == exit:
                        line2.append(f' \033[48;2;255;0;0m    {reset_collor}')
                    else:
                        line2.append('     ')

            line1.append(f'\033[38;2;{white}m█\033[0m')
            line2.append(f'\033[38;2;{white}m█\033[0m')
            render_maze.append(line1)
            render_maze.append(line2)
            render_maze.append(line2)
        render_maze.append(final_line)
        return render_maze

    def render_path(self, entry: tuple, exit: tuple,
                    rgb: tuple) -> list[list[str]]:
        r, g, b = rgb
        set_collor = f'\033[48;2;{r};{g};{b}m'
        reset_collor = '\033[0m'
        white = '255;255;255'
        render_maze = []
        w = self.maze.width
        h = self.maze.heigth
        path = self.path.copy()
        maze = self.maze

        final_line = []
        for _ in range(0, w):
            final_line.append(f'\033[38;2;{white}m█████{reset_collor}')
        final_line.append(f'\033[38;2;{white}m█{reset_collor}')

        for y in range(0, h):
            line1 = []
            line2 = []

            for x in range(0, w):
                if maze.maze[y][x]._walls['N']:
                    line1.append(f'\033[38;2;{white}m█████{reset_collor}')
                else:
                    line1.append(f'\033[38;2;{white}m█    {reset_collor}')

                if maze.maze[y][x]._walls['W']:
                    if maze.maze[y][x].close_block():
                        line2.append(f'\033[38;2;{white}m█{reset_collor}\
\033[48;2;100;100;100m    {reset_collor}')
                    elif (x, y) == entry:
                        line2.append(f'\033[38;2;{white}m█{reset_collor}\
\033[48;2;0;0;255m    {reset_collor}')
                    elif (x, y) == exit:
                        line2.append(f'\033[38;2;{white}m█{reset_collor}\
\033[48;2;255;0;0m    {reset_collor}')
                    elif (x, y) in path:
                        line2.append(f'\033[38;2;{white}m█{reset_collor}\
{set_collor}    {reset_collor}')
                        path.remove((x, y))
                    else:
                        line2.append(f'\033[38;2;{white}m█{reset_collor}    ')
                else:
                    if (x, y) == entry:
                        line2.append(f' \033[48;2;0;0;255m    {reset_collor}')
                    elif (x, y) == exit:
                        line2.append(f' \033[48;2;255;0;0m    {reset_collor}')
                    elif (x, y) in path:
                        line2.append(f' {set_collor}    {reset_collor}')
                    else:
                        line2.append('     ')

            line1.append(f'\033[38;2;{white}m█{reset_collor}')
            line2.append(f'\033[38;2;{white}m█{reset_collor}')
            render_maze.append(line1)
            render_maze.append(line2)
            render_maze.append(line2)
        render_maze.append(final_line)
        return
