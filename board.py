# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

"""
board.py

This file contains the Board class.
The Board class handles the grid, ships, placement, attacks, and sunk ships.
"""

import random
from settings import GRID_SIZE, SHIP_SIZES
from ship import Ship


class Board:
    """
    Represents one Battleship board.
    """

    def __init__(self):
        """
        Create an empty board.

        The grid stores:
            ' ' = empty
            'S' = ship
            'X' = hit
            'O' = miss / blocked water around a sunk ship
        """
        self.grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
        self.occupied_cells = set()
        self.attacked_cells = set()

        # These cells are too close to another ship.
        # Ships cannot be placed on these cells.
        self.blocked_placement_cells = set()

    def get_ship_cells(self, start_row, start_col, length, orientation):
        """
        Calculate all cells a ship would occupy.

        Args:
            start_row (int): Starting row.
            start_col (int): Starting column.
            length (int): Ship length.
            orientation (str): 'H' for horizontal or 'V' for vertical.

        Returns:
            list: List of (row, col) cells.
        """
        if orientation == 'H':
            return [(start_row, start_col + i) for i in range(length)]

        return [(start_row + i, start_col) for i in range(length)]

    def get_surrounding_cells(self, ship_cells):
        """
        Get every square surrounding a ship, including diagonals.

        Args:
            ship_cells (list): Cells occupied by the ship.

        Returns:
            set: Surrounding cells that are still inside the board.
        """
        surrounding_cells = set()

        for row, col in ship_cells:
            for row_change in [-1, 0, 1]:
                for col_change in [-1, 0, 1]:
                    new_row = row + row_change
                    new_col = col + col_change

                    if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                        surrounding_cells.add((new_row, new_col))

        # Remove the actual ship cells.
        surrounding_cells.difference_update(ship_cells)

        return surrounding_cells

    def can_place_ship(self, ship_cells):
        """
        Check whether a ship can be placed.

        A valid placement:
            - stays inside the board
            - does not overlap another ship
            - does not touch another ship, not even diagonally

        Args:
            ship_cells (list): List of (row, col) cells.

        Returns:
            bool: True if placement is valid.
        """
        for row, col in ship_cells:
            if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
                return False

            if (row, col) in self.occupied_cells:
                return False

            if (row, col) in self.blocked_placement_cells:
                return False

        return True

    def place_ship(self, size, row, col, orientation):
        """
        Try to place a ship on the board.

        Args:
            size (int): Length of the ship.
            row (int): Starting row.
            col (int): Starting column.
            orientation (str): 'H' or 'V'.

        Returns:
            bool: True if the ship was placed.
        """
        ship_cells = self.get_ship_cells(row, col, size, orientation)

        if not self.can_place_ship(ship_cells):
            return False

        new_ship = Ship(size, ship_cells)
        self.ships.append(new_ship)
        self.occupied_cells.update(ship_cells)

        # Mark the ship on the grid.
        for r, c in ship_cells:
            self.grid[r][c] = 'S'

        # Block nearby cells so future ships cannot touch this one.
        nearby_cells = self.get_surrounding_cells(ship_cells)
        self.blocked_placement_cells.update(nearby_cells)

        return True

    def place_random_ship(self, size):
        """
        Place one ship randomly on the board.

        Args:
            size (int): Length of the ship.
        """
        valid_ship_found = False

        while not valid_ship_found:
            orientation = random.choice(['H', 'V'])

            if orientation == 'H':
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - size)
            else:
                row = random.randint(0, GRID_SIZE - size)
                col = random.randint(0, GRID_SIZE - 1)

            valid_ship_found = self.place_ship(size, row, col, orientation)

    def place_random_fleet(self):
        """
        Randomly place all ships from SHIP_SIZES.
        """
        for size in SHIP_SIZES:
            self.place_random_ship(size)

    def find_ship_at_cell(self, cell):
        """
        Find which ship is located at a specific cell.

        Args:
            cell (tuple): A (row, col) location.

        Returns:
            Ship or None: The ship at that cell, if one exists.
        """
        for ship in self.ships:
            if ship.contains_cell(cell):
                return ship

        return None

    def mark_water_around_sunk_ship(self, ship):
        """
        Mark all water cells around a sunk ship as misses.

        Once a ship is sunk, the surrounding squares cannot contain ships,
        so they are marked as unavailable.

        Args:
            ship (Ship): The ship that was sunk.
        """
        surrounding_cells = self.get_surrounding_cells(ship.cells)

        for row, col in surrounding_cells:
            if (row, col) not in self.occupied_cells:
                self.grid[row][col] = 'O'
                self.attacked_cells.add((row, col))

    def receive_attack(self, row, col):
        """
        Handle an attack on this board.

        Args:
            row (int): Attacked row.
            col (int): Attacked column.

        Returns:
            tuple:
                result (str): 'repeat', 'hit', 'miss', or 'sunk'
                ship (Ship or None): The ship that was sunk, if any.
        """
        cell = (row, col)

        if cell in self.attacked_cells:
            return "repeat", None

        self.attacked_cells.add(cell)

        if cell in self.occupied_cells:
            self.grid[row][col] = 'X'

            hit_ship = self.find_ship_at_cell(cell)

            if hit_ship is not None:
                hit_ship.hit(cell)

                if hit_ship.is_sunk():
                    self.mark_water_around_sunk_ship(hit_ship)
                    return "sunk", hit_ship

            return "hit", hit_ship

        self.grid[row][col] = 'O'
        return "miss", None

    def all_ships_sunk(self):
        """
        Check whether every ship on this board has been sunk.

        Returns:
            bool: True if all ships are sunk.
        """
        if len(self.ships) == 0:
            return False

        return all(ship.is_sunk() for ship in self.ships)
