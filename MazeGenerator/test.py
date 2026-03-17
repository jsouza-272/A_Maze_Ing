from .MazeGenerator import MazeGenerator


if __name__ == "__main__":
    generator = MazeGenerator(20, 15, (0, 0), (19, 14), True)
    generator.generate_maze()
    generator.show_maze()
