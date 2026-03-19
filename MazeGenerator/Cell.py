class Cell():
    def __init__(self) -> None:
        self._walls = {'N': 1,
                       'E': 1,
                       'S': 1,
                       'W': 1}
        self._visited = False

    def break_wall(self, direction: str) -> None:
        self._walls.update({direction: 0})

    def visited(self) -> None:
        self._visited = True

    def get_hex(self) -> str:
        bit_weights = {'N': 1,
                       'E': 2,
                       'S': 4,
                       'W': 8}
        total = sum([self._walls[key] * value
                     for key, value in bit_weights.items()])
        return '0123456789abcdef'[total]

    def get_path(self) -> list[str]:
        return [key for key in self._walls.keys()
                if self._walls[key] == 0]
