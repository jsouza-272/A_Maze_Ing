"""
Custom exceptions for the mazegen package.

Defines error types raised during maze generation and pathfinding to allow
callers to handle specific failure conditions cleanly.
"""


class AstarError(Exception):
    """Raised when the A* algorithm cannot find a path through the maze."""
    pass


class FtError(Exception):
    """Raised when the "42" obstacle pattern cannot be placed in the maze."""
    pass
