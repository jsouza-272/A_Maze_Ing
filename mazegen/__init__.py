"""
mazegen package.

Exports the public API of the maze-generation subsystem:
- MazeGenerator: high-level maze builder and serializer
- Astar: A* pathfinding algorithm
"""
from .MazeGenerator import MazeGenerator
from .algorithms import Astar


__all__ = ['MazeGenerator', 'Astar']
