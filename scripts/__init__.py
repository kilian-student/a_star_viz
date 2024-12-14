"""
a_star_viz: A Python package for visualizing the A* algorithm.

Modules:
- Graph: Define and manage the grid for pathfinding.
- A_star: Implementation of the A* algorithm.
- MainWindow(QMainWindow): Handle Qt Widgets


Author: Kilian Ernst
Version: 1.0.0
"""

# Package metadata
__author__ = "Kilian Ernst"
__version__ = "1.0.0"
__email__ = "kilianernst96@gmail.com"
__license__ = "MIT"

# Expose key functions and classes for easier imports
from .utils.graph import Graph
from .utils.a_start_algorithm import A_star
from .utils.main_window import MainWindow

__all__ = ["Graph", "A_star", "MainWindow"]
