from .Maze import Maze
import random


class Dfs():
    def __init__(self, seed: int = 42):
        self.seed = random.Random(seed)

    def generate_maze(self, maze: Maze,
                      entry: tuple[int, int], exit: tuple[int, int]) -> None:
        stack: list = [entry]
        candidates = maze.unvisited_neighbors(*stack[-1])
        while stack:
            cx, cy = stack[-1]
            maze.maze[cy][cx].visited()
            candidates = maze.unvisited_neighbors(cx, cy)
            if len(candidates) == 0 or (cx, cy) == exit:
                stack.pop()
            else:
                nx, ny = self.seed.choice(candidates)
                maze.maze[cy][cx].break_wall(maze.direction(
                    (cx, cy), (nx, ny)))
                maze.maze[ny][nx].break_wall(maze.direction(
                    (nx, ny), (cx, cy)))
                stack.append((nx, ny))
