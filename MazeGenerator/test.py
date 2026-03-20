from .MazeGenerator import MazeGenerator
from .Ui import Ui
from .pathfinder.Astar import Astar


if __name__ == "__main__":
    entry = (0, 0)
    exit = (19, 14)
    generator = MazeGenerator(20, 15, entry, exit, True)
    generator.generate_maze()
    with open('maze.txt', 'w') as file:
        file.write(generator.get_maze())
    pathfinder = Astar()
    ui = Ui(generator.maze, pathfinder.algorithm(generator.maze, entry, exit))
    ui.show_maze(True)
