"""
mazegen.maze package.

Exports the core maze data structures used by the mazegen package:
- Maze: 2-D grid of Cell objects representing the maze
- Cell: individual cell with wall and visited state
"""
from .Maze import Maze
from .Cell import Cell


__all__ = ['Maze', 'Cell']
