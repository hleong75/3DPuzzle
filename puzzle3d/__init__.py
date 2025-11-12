"""
3D Puzzle Generator

A tool to transform 3D objects into interlocking 3D puzzles for wood manufacturing.
Supports UGEARS-style mechanical wooden puzzles with proper tolerances.
"""

__version__ = "0.1.0"

from .puzzle_generator import PuzzleGenerator
from .slicer import PuzzleSlicer
from .interlocking import InterlockingGenerator
from .config import PuzzleConfig

__all__ = ['PuzzleGenerator', 'PuzzleSlicer', 'InterlockingGenerator', 'PuzzleConfig']
