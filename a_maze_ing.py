from parser import load_and_parse_config
from MazeGenerator import MazeGenerator, Ui, Astar
import os


if __name__ == "__main__":
    try:
        show = False
        choise = 1
        while choise != 0:
            if choise == 1:
                os.system('clear')
                config = load_and_parse_config()
                generator = MazeGenerator(**config)
                generator.generate_maze()
                generator.save_maze()
                ui = Ui(generator.maze, Astar().
                        algorithm(generator.maze,
                                  config['entry'], config['exit']))
                ui.show_maze(config['entry'], config['exit'], show)
            elif choise == 2:
                if not show:
                    show = True
                    ui.show_maze(config['entry'], config['exit'], show)
                else:
                    show = False
                    ui.show_maze(config['entry'], config['exit'], show)
            choise = int(input())
    except ValueError as e:
        print(e)
