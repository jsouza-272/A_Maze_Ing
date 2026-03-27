"""
mazegen.algorithms package.

Exports the pathfinding and generation algorithms used by the mazegen package:
- Astar: A* shortest-path solver
- Dfs: depth-first search maze carver
- Prim: randomized Prim's algorithm maze carver
"""
from .Astar import Astar
from .Dfs import Dfs
from .Prim import Prim

__all__ = ['Astar', 'Dfs', 'Prim']
