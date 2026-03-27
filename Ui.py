"""
Terminal UI utilities for rendering and interacting with a maze.

This module provides a simple text-based interface that:
- prints a menu to the user
- validates user input
- renders the maze using ANSI color codes
- optionally overlays the solution path from entry to exit
"""
from mazegen.maze.Maze import Maze


class Ui():
    """
    Terminal UI for displaying a Maze and an optional solution path.

    The UI is responsible for:
    - printing the menu and collecting user choices
    - rendering the maze with ANSI colors
    - rendering the maze with the solution path overlay

    Args:
        maze (Maze): Maze instance to render.
        path (list[tuple[int, int]]): List of coordinates representing the
            solution path.
    """

    def __init__(self, maze: Maze, path: list) -> None:
        """
        Initialize the UI with a maze instance and a precomputed path.

        Args:
            maze (Maze): Maze to display.
            path (list[tuple[int, int]]): Path coordinates to
            optionally render.
        """
        self.maze = maze
        self.path = path

    def menu(self, show: bool, algorithm: str) -> None:
        """
        Print the interactive menu to stdout.

        Args:
            show (bool): Whether the path overlay is currently enabled.
            algorithm (str): Name of the currently active generation algorithm.
        """
        print("\n=== A-Maze-Ing ===")
        print("1. Re-generate a new maze")
        print(f"2. Show path from entry to exit ({show})")
        print(f"3. Change algorithm (current: {algorithm})")
        print("4. Rotate maze colors")
        print("5. Add an RGB color to the color list")
        print("6. Remove the last RGB color from the color list")
        print("0. Quit")
        print('\nChoice (0-6):', end=' ')

    def input_validate(self) -> int:
        """
        Read and validate the user's menu choice.

        Keeps prompting until a valid integer is provided.

        Returns:
            int: The validated menu choice.
        """
        while True:
            try:
                choice = int(input())
                return choice
            except ValueError:
                print('Please insert a number:', end=' ')

    def show_maze(self, entry: tuple, exit: tuple,
                  rgb: tuple, path: bool = False) -> None:
        """
        Print the maze to stdout, optionally showing the solution path.

        Args:
            entry (tuple[int, int]): Entry coordinate (x, y).
            exit (tuple[int, int]): Exit coordinate (x, y).
            rgb (tuple[int, int, int]): Maze wall color as (r, g, b).
            path (bool): If True, overlay the solution path.
        """
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
        """
        Build a rendered representation of the maze without the solution path.

        The output is a 2-D list of strings where each string contains ANSI
        escape codes and block characters.

        Args:
            entry (tuple[int, int]): Entry coordinate (x, y).
            exit (tuple[int, int]): Exit coordinate (x, y).
            rgb (tuple[int, int, int]): Maze wall color as (r, g, b).

        Returns:
            list[list[str]]: Lines and segments to be printed to display the
                maze.
        """
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
        """
        Build a rendered representation of the maze with the solution path.

        Args:
            entry (tuple[int, int]): Entry coordinate (x, y).
            exit (tuple[int, int]): Exit coordinate (x, y).
            rgb (tuple[int, int, int]): Maze wall color as (r, g, b).

        Returns:
            list[list[str]]: Lines and segments to be printed with a path
                overlay.
        """
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
