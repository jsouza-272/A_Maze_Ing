from .maze.Maze import Maze
import os


class Ui():
    def __init__(self, maze: Maze, path: list) -> None:
        self.maze = maze
        self.path = path

    def clean(self) -> None:
        os.system('clean')

    def render(self) -> list:
        w = self.maze.width
        h = self.maze.heigth
        b = 255
        render_maze = []

        top = f'\033[38;2;255;255;{b}m█\033[0m'
        for c in range(w):
            top += f"\033[38;2;255;255;{b}m████\033[0m"
        render_maze.append(top)

        for y in range(h):
            mid = ""
            bottom = f'\033[38;2;255;255;{b}m█\033[0m'

            for x in range(w):
                cell = self.maze.maze[y][x]
                if cell.close_block():
                    mid += "\033[38;2;255;255;255m█\
\033[38;2;90;90;90m███\033[0m"
                elif cell._walls['W']:
                    mid += f'\033[38;2;255;255;{b}m█\033[0m   '
                else:
                    mid += '    '

                if cell._walls['S']:
                    bottom += f"\033[38;2;255;255;{b}m████\033[0m"
                else:
                    bottom += f"   \033[38;2;255;255;{b}m█\033[0m"

            last = self.maze.maze[y][-1]
            if last._walls['E']:
                mid += f'\033[38;2;255;255;{b}m█\033[0m'
            else:
                " "
            render_maze.append(mid)
            render_maze.append(bottom)
        return render_maze

    def render_path(self, entry: tuple, exit: tuple) -> list:
        w = self.maze.width
        h = self.maze.heigth
        b = 255
        render_maze = []

        top = f'\033[38;2;255;255;{b}m█\033[0m'
        for c in range(w):
            cell = self.maze.maze[0][c]
            if cell._walls['N']:
                top += f"\033[38;2;255;255;{b}m████\033[0m"
            else:
                top += f"   \033[38;2;255;255;{b}m█\033[0m"
        render_maze.append(top)

        for y in range(h):
            mid = ""
            bottom = f'\033[38;2;255;255;{b}m█\033[0m'

            for x in range(w):
                cell = self.maze.maze[y][x]
                if cell.close_block():
                    mid += "\033[38;2;255;255;255m█\
\033[38;2;90;90;90m███\033[0m"
                elif cell._walls['W']:
                    if (x, y) in self.path:
                        mid += '\033[38;2;255;255;255m█\
\033[38;2;0;255;0m███\033[0m'
                    else:
                        if (x, y) == entry:
                            mid += '█\033[48;2;0;0;255m   \033[0m'
                        elif (x, y) == exit:
                            mid += '█\033[48;2;255;0;0m   \033[0m'
                        else:
                            mid += f'\033[38;2;255;255;{b}m█\033[0m   '
                else:
                    if (x, y) in self.path:
                        # mid += '\033[38;2;0;255;0m ███\033[0m'
                        mid += '\033[48;2;0;255;0m    \033[0m'
                    else:
                        if (x, y) == entry:
                            mid += '\033[48;2;0;0;255m    \033[0m'
                        if (x, y) == exit:
                            mid += '\033[48;2;255;0;0m    \033[0m'
                        else:
                            mid += '    '

                if cell._walls['S']:
                    bottom += f"\033[38;2;255;255;{b}m████\033[0m"
                else:
                    if (x, y) in self.path:
                        bottom += '\033[48;2;0;255;0m   \
\033[38;2;255;255;255m█\033[0m'
                        self.path.remove((x, y))
                    else:
                        if (x, y) == entry:
                            bottom += '\033[48;2;0;255;0m   \
\033[38;2;255;255;255m█\033[0m'
                        else:
                            bottom += f"   \033[38;2;255;255;{b}m█\033[0m"

            last = self.maze.maze[y][-1]
            if last._walls['E']:
                mid += f'\033[38;2;255;255;{b}m█\033[0m'
            else:
                mid += " "
            render_maze.append(mid)
            render_maze.append(bottom)
        print(len(render_maze), len(bottom), len(mid))
        return render_maze

    def show_maze(self, entry: tuple, exit: tuple, path: bool = False) -> None:
        if path:
            for line in self.render_path(entry, exit):
                print(line)
        else:
            for line in self.render():
                print(line)
