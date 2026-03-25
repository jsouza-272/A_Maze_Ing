"""
Main entry point for the A-Maze-Ing application.

This script orchestrates the whole maze generation and solving pipeline:
- loads and validates configuration from a config file
- generates a maze (perfect or imperfect) with an optional "42" obstacle
- solves the maze using the A* algorithm
- writes the resulting cardinal path to the configured output file
- renders an interactive terminal UI for visualization

Run:
    python3 a_maze_ing.py config.txt

Raises:
    ValueError: If configuration values are invalid.
"""
from parser import load_and_parse_config
from mazegen import MazeGenerator, Astar
from Ui import Ui
import os


if __name__ == "__main__":
    try:
        show = False
        choice = 1
        rgb = (255, 255, 255)
        while choice != 0:
            os.system('clear')
            if choice == 1:
                config = load_and_parse_config()
                generator = MazeGenerator(**config)
                generator.generate_maze()
                generator.save_maze()
                path = Astar().algorithm(generator.maze,
                                         config['entry'], config['exit'])

                with open(config['output_file'], 'a') as output_file:
                    output_file.write(Astar.make_cardinal_path(
                        path.copy(), config['exit']))
                ui = Ui(generator.maze, path)

            elif choice == 2:
                if not show:
                    show = True
                else:
                    show = False

            elif choice == 3:
                if rgb == (255, 255, 255):
                    rgb = (240, 224, 0)
                else:
                    rgb = (255, 255, 255)

            ui.show_maze(config['entry'], config['exit'], rgb, show)
            ui.menu(show)
            choice = ui.input_validate()
    except ValueError as e:
        print(e)
