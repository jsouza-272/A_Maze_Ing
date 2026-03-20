from parser import load_and_parse_config
from MazeGenerator import MazeGenerator, Ui, Astar
import sys


if __name__ == "__main__":
    try:
        config = load_and_parse_config(sys.argv)
        generator = MazeGenerator(**config)
        generator.generate_maze()
        generator.save_maze()
        ui = Ui(generator.maze, Astar().algorithm(generator.maze,
                                                  config['entry'], config['exit']))
        ui.show_maze(True)
    except ValueError as e:
        print(e)
