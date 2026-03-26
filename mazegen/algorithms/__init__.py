"""
mazegen.algorithms package.

Exports the pathfinding and generation algorithms used by the mazegen package:
- Astar: A* shortest-path solver
"""
from .Astar import Astar
from .Dfs import Dfs
from .Prim import Prim

__all__ = ['Astar', 'Dfs', 'Prim']
