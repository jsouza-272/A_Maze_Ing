from .MazeGenerator import MazeGenerator


if __name__ == "__main__":
    generator = MazeGenerator(50, 50, (0, 0), (49, 49), True)
    generator.generate_maze()
    print(generator.get_maze())
