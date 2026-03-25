from mazegen.maze.Maze import Maze


class Ui():
    def __init__(self, maze: Maze, path: list) -> None:
        self.maze = maze
        self.path = path

    def menu(self, show: bool) -> None:
        print("\n=== A-Maze-Ing ===")
        print("1. Re-generate a new maze")
        print(f"2. Show path from entry to exit ({show})")
        print("3. Rotate maze colors")
        print("0. Quit")
        print('\nChoice (0-3):', end=' ')

    def input_validate(self) -> int:
        while True:
            try:
                choice = int(input())
                return choice
            except ValueError:
                print('Please insert a number:', end=' ')

    def show_maze(self, entry: tuple, exit: tuple,
                  rgb: tuple, path: bool = False) -> None:
        if path:
            for line in self.render_path(entry, exit, rgb):
                for _ in line:
                    print(_, end='')
                print()
        else:
            for line in self.render(entry, exit, rgb):
                for _ in line:
                    print(_, end='')
                print()

    def render(self, entry: tuple, exit: tuple, rgb: tuple) -> list[list[str]]:
        r, g, b = rgb
        render_maze = []
        w = self.maze.width
        h = self.maze.heigth
        maze = self.maze
        reset_color = '\033[0m'
        set_color = f'{r};{g};{b}'

        final_line = []

        for _ in range(0, w):
            final_line.append(f'\033[38;2;{set_color}m█████\033[0m')
        final_line.append(f'\033[38;2;{set_color}m█\033[0m')

        for y in range(0, h):
            line1 = []
            line2 = []

            for x in range(0, w):
                if maze.maze[y][x]._walls['N']:
                    line1.append(f'\033[38;2;{set_color}m█████\033[0m')
                else:
                    line1.append(f'\033[38;2;{set_color}m█\033[0m    ')

                if maze.maze[y][x]._walls['W']:
                    if maze.maze[y][x].close_block():
                        line2.append(f'\033[38;2;{set_color}m█\033[0m\
\033[48;2;100;100;100m    \033[0m')
                    elif (x, y) == entry:
                        line2.append(f'\033[38;2;{set_color}m█{reset_color}\
\033[48;2;0;0;255m    {reset_color}')
                    elif (x, y) == exit:
                        line2.append(f'\033[38;2;{set_color}m█{reset_color}\
\033[48;2;255;0;0m    {reset_color}')
                    else:
                        line2.append(f'\033[38;2;{set_color}m█\033[0m    ')
                else:
                    if (x, y) == entry:
                        line2.append(f' \033[48;2;0;0;255m    {reset_color}')
                    elif (x, y) == exit:
                        line2.append(f' \033[48;2;255;0;0m    {reset_color}')
                    else:
                        line2.append('     ')

            line1.append(f'\033[38;2;{set_color}m█\033[0m')
            line2.append(f'\033[38;2;{set_color}m█\033[0m')
            render_maze.append(line1)
            render_maze.append(line2)
            render_maze.append(line2)
        render_maze.append(final_line)
        return render_maze

    def render_path(self, entry: tuple, exit: tuple,
                    rgb: tuple) -> list[list[str]]:
        r, g, b = rgb
        path_color = '\033[48;2;0;255;0m'
        reset_color = '\033[0m'
        set_color = f'{r};{g};{b}'
        render_maze = []
        w = self.maze.width
        h = self.maze.heigth
        path = self.path.copy()
        maze = self.maze

        final_line = []
        for _ in range(0, w):
            final_line.append(f'\033[38;2;{set_color}m█████{reset_color}')
        final_line.append(f'\033[38;2;{set_color}m█{reset_color}')

        for y in range(0, h):
            line1 = []
            line2 = []

            for x in range(0, w):
                if maze.maze[y][x]._walls['N']:
                    line1.append(f'\033[38;2;{set_color}m█████{reset_color}')
                else:
                    line1.append(f'\033[38;2;{set_color}m█    {reset_color}')

                if maze.maze[y][x]._walls['W']:
                    if maze.maze[y][x].close_block():
                        line2.append(f'\033[38;2;{set_color}m█{reset_color}\
\033[48;2;100;100;100m    {reset_color}')
                    elif (x, y) == entry:
                        line2.append(f'\033[38;2;{set_color}m█{reset_color}\
\033[48;2;0;0;255m    {reset_color}')
                    elif (x, y) == exit:
                        line2.append(f'\033[38;2;{set_color}m█{reset_color}\
\033[48;2;255;0;0m    {reset_color}')
                    elif (x, y) in path:
                        line2.append(f'\033[38;2;{set_color}m█{reset_color}\
{path_color}    {reset_color}')
                        path.remove((x, y))
                    else:
                        line2.append(f'\033[38;2;{set_color}m█\
{reset_color}    ')
                else:
                    if (x, y) == entry:
                        line2.append(f' \033[48;2;0;0;255m    {reset_color}')
                    elif (x, y) == exit:
                        line2.append(f' \033[48;2;255;0;0m    {reset_color}')
                    elif (x, y) in path:
                        line2.append(f' {path_color}    {reset_color}')
                    else:
                        line2.append('     ')

            line1.append(f'\033[38;2;{set_color}m█{reset_color}')
            line2.append(f'\033[38;2;{set_color}m█{reset_color}')
            render_maze.append(line1)
            render_maze.append(line2)
            render_maze.append(line2)
        render_maze.append(final_line)
        return render_maze
