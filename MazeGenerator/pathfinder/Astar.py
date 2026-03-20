from ..maze.Maze import Maze
from ..Errors import AstarError


class Astar():
    @staticmethod
    def manhattan(pos: tuple[int, int], goal: tuple[int, int]) -> int:
        result = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        return result

    def algorithm(self, maze: Maze, entry: tuple, exit: tuple) -> list[tuple]:
        g = 0
        h = self.manhattan(entry, exit)
        f_score = {entry: g + h}
        g_score = {entry: g}
        openset = {entry}
        closeset: set = set()
        came_from = {}
        current_node = min(f_score, key=lambda k: f_score[k])

        while openset:
            current_node = min(f_score, key=lambda k: f_score[k])
            x, y = current_node
            neighbors = maze.get_neighbors(x, y, closeset)

            for n in neighbors:
                if n not in openset:
                    openset.add(n)
                    g_score[n] = g_score[current_node] + 1
                    f_score[n] = g_score[n] + self.manhattan(n, exit)
                    came_from[n] = current_node

                elif n in g_score and g_score[current_node] + 1 < g_score[n]:
                    g_score[n] = g_score[current_node] + 1
                    f_score[n] = g_score[n] + self.manhattan(n, exit)
                    came_from[n] = current_node

            openset.discard(current_node)
            f_score.pop(current_node)
            closeset.add(current_node)

            if current_node == exit:
                return self.make_path(came_from, entry, exit)

        raise AstarError("Error: path not exist")

    def make_path(self, came_from: dict[tuple, tuple],
                  entry: tuple, exit: tuple) -> list[tuple]:
        path = {}
        current = exit
        while True:
            path[current] = came_from[current]
            current = came_from[current]
            if current == entry:
                break
        list_path = list(path.values())
        list_path.pop()
        return list_path

    def make_cardinal_path(self, list_path: list[tuple]) -> str:
        cardinal_path = ''
        while list_path:
            xy = list_path.pop()
            if list_path:
                cardinal_path += Maze.direction(xy, list_path[-1])
            else:
                cardinal_path += Maze.direction(xy, exit)
        return cardinal_path
