# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

"""
ship.py

This file contains the Ship class.
Each Ship object stores its size, its cells, and which cells have been hit.
"""


class Ship:
    """
    Represents one ship on a Battleship board.
    """

    def __init__(self, size, cells):
        """
        Create a new ship.

        Args:
            size (int): The length of the ship.
            cells (list): List of (row, col) tuples occupied by the ship.
        """
        self.size = size
        self.cells = cells
        self.hits = set()

    def contains_cell(self, cell):
        """
        Check if this ship occupies a specific cell.

        Args:
            cell (tuple): A (row, col) location.

        Returns:
            bool: True if the ship is on that cell.
        """
        return cell in self.cells

    def hit(self, cell):
        """
        Record a hit on the ship.

        Args:
            cell (tuple): The attacked cell.

        Returns:
            bool: True if the attack hit this ship.
        """
        if self.contains_cell(cell):
            self.hits.add(cell)
            return True

        return False

    def is_sunk(self):
        """
        Check whether the entire ship has been hit.

        Returns:
            bool: True if all ship cells have been hit.
        """
        return len(self.hits) == self.size
