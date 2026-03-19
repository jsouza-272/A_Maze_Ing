from .MazeGenerator import MazeGenerator
from .Astar import Astar


if __name__ == "__main__":
    entry = (1, 1)
    exit = (19, 14)
    generator = MazeGenerator(20, 25, entry, exit, True)
    generator.generate_maze()
    print(generator.get_maze())
    print(Astar().algorithm(generator.maze, entry, exit))
