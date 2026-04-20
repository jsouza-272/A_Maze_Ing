"""
Main entry point for the A-Maze-Ing application.

This script orchestrates the whole maze generation and solving pipeline:
- loads and validates configuration from a config file
- generates a maze (perfect or imperfect) with an optional "42" obstacle
- solves the maze using the A* algorithm
- writes the resulting cardinal path to the configured output file
- renders an interactive terminal UI for visualization

The generation algorithm can be toggled interactively between DFS and Prim
using menu option 3.

Run:
    python3 a_maze_ing.py config.txt

Raises:
    ValueError: If configuration values are invalid.
"""
from parser import load_and_parse_config
from mazegen import MazeGenerator, Astar
from mazegen.algorithms import Dfs, Prim
from Ui import Ui
from time import sleep
import os


if __name__ == "__main__":
    try:
        show = True
        animation = False
        choice = 1
        rgb_list = [(255, 255, 255), (240, 224, 0)]
        rgb_index = 0
        rgb = rgb_list[rgb_index]
        algorithm: type[Dfs] | type[Prim] = Prim
        while choice != 0:
            message = None
            if choice == 3:
                if algorithm == Dfs:
                    algorithm = Prim
                else:
                    algorithm = Dfs
                choice = 1

            if choice == 1:
                config = load_and_parse_config()
                generator = MazeGenerator(**config, algorithm=algorithm)
                message = generator.generate_maze(animation)
                try:
                    os.remove(generator.output_file)
                except FileNotFoundError:
                    pass
                generator.save_maze()
                path = Astar().algorithm(generator.maze,
                                         config['entry'], config['exit'])
                nodes = []
                while True:
                    try:
                        os.system('clear')
                        nodes.append(next(path))
                        if animation:
                            Ui(generator.maze,
                               []).show_maze(config['entry'],
                                             config['exit'],
                                             rgb_list[0], True, nodes)
                            sleep(0.07)
                    except StopIteration as error:
                        nodes.clear()
                        path = error.value
                        break

                with open(config['output_file'], 'a') as output_file:
                    output_file.write(Astar.make_cardinal_path(
                        path.copy(), config['exit']))
                ui = Ui(generator.maze, path)

            elif choice == 2:
                if not show:
                    show = True
                else:
                    show = False

            elif choice == 4:
                rgb_index += 1
                if rgb_index >= len(rgb_list):
                    rgb_index = 0
                rgb = rgb_list[rgb_index]

            elif choice == 5:
                while True:
                    try:
                        r = int(input('R: '))
                        if r > 255 or r < 0:
                            raise KeyError(
                                f'Error: R ({r}) out of range 0-255')
                        g = int(input('G: '))
                        if g > 255 or g < 0:
                            raise KeyError(
                                f'Error: G ({g}) out of range 0-255')
                        b = int(input('B: '))
                        if b > 255 or b < 0:
                            raise KeyError(
                                f'Error: B ({b}) out of range 0-255')
                        break
                    except ValueError:
                        print('Please insert a number in range 0-255')
                    except KeyError as e:
                        print(e.args[0])
                if (r, g, b) not in rgb_list:
                    rgb_list.append((r, g, b))
                    message = f'({r}, {g}, {b}) has been added to the list'
                else:
                    message = f'({r}, {g}, {b}) is already on the list'

            elif choice == 6:
                try:
                    if len(rgb_list) == 2:
                        raise ValueError('It is not possible to \
remove the default colors')
                    else:
                        message = f'{rgb_list.pop()} removed'
                        if rgb not in rgb_list:
                            rgb = rgb_list[-1]
                except ValueError as e:
                    message = e.args[0]

            elif choice == 7:
                if not animation:
                    animation = True
                else:
                    animation = False

            os.system('clear')
            ui.show_maze(config['entry'], config['exit'], rgb, show)
            if message is not None:
                print(message)
            ui.menu(show, algorithm.__name__, animation)
            choice = ui.input_validate()
    except ValueError as e:
        print(e)
