from mazegen.maze import Maze
import random


class Prim():
    def __init__(self, seed: int | None = None):
        self.seed = random.Random(seed)

    def generate_maze(self, maze: Maze,
                      entry: tuple[int, int], exit: tuple[int, int]) -> None:
        maze.maze[entry[1]][entry[0]].visited()
        frontiers = [(entry, neighbor)
                     for neighbor in maze.unvisited_neighbors(*entry)]
        while frontiers:
            chosen1, chosen2 = self.seed.choice(frontiers)
            frontiers.remove((chosen1, chosen2))
            if not maze.maze[chosen2[1]][chosen2[0]]._visited:
                maze.maze[chosen2[1]][chosen2[0]].visited()
                frontiers.extend([(chosen2, neighbor) for neighbor in maze.
                                  unvisited_neighbors(*chosen2)])
                maze.maze[chosen1[1]][chosen1[0]].break_wall(
                    maze.direction(chosen1, chosen2))
                maze.maze[chosen2[1]][chosen2[0]].break_wall(
                    maze.direction(chosen2, chosen1))
