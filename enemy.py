# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

"""
enemy.py

This file contains the Enemy class.
The Enemy is a type of Player, but it chooses attacks automatically.
"""

import random
from settings import GRID_SIZE
from player import Player


class Enemy(Player):
    """
    Represents the computer opponent.
    """

    def __init__(self, name="Enemy"):
        """
        Create the enemy player.
        """
        super().__init__(name)

        # Stores successful hits on the ship the enemy is currently hunting.
        self.hit_stack = []

        # Stores squares the enemy wants to try next.
        self.target_queue = []

        # Stores the direction of the ship after two hits: "H" or "V".
        self.direction = None

    def choose_attack(self, player_board):
        """
        Choose the enemy's next attack.

        If the enemy is hunting a ship, it uses target_queue first.
        If there are no planned targets, it picks a random available square.

        Args:
            player_board (Board): The player's board.

        Returns:
            tuple: A (row, col) attack location.
        """
        # Try planned target squares first.
        while len(self.target_queue) > 0:
            row, col = self.target_queue.pop(0)

            if (row, col) not in player_board.attacked_cells:
                return row, col

        # Otherwise, build a list of every square not attacked yet.
        available_moves = []

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row, col) not in player_board.attacked_cells:
                    available_moves.append((row, col))

        return random.choice(available_moves)

    def process_attack_result(self, row, col, result, player_board):
        """
        Update enemy strategy based on the attack result.

        Args:
            row (int): Row attacked.
            col (int): Column attacked.
            result (str): 'hit', 'miss', or 'sunk'.
            player_board (Board): The player's board.
        """
        if result == "sunk":
            self.hit_stack = []
            self.target_queue = []
            self.direction = None
            return

        if result == "miss":
            return

        if result == "hit":
            self.hit_stack.append((row, col))

            # First hit: try direct neighbors only.
            if len(self.hit_stack) == 1:
                self.add_first_hit_targets(row, col, player_board)

            # Two or more hits: figure out direction and stay in a line.
            elif len(self.hit_stack) >= 2:
                self.find_direction()
                self.add_line_targets(player_board)

    def add_first_hit_targets(self, row, col, player_board):
        """
        After the first hit, only try the four direct neighbors.
        No diagonal squares are added.

        Args:
            row (int): Hit row.
            col (int): Hit column.
            player_board (Board): The player's board.
        """
        possible_targets = [
            (row - 1, col),  # up
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1)   # right
        ]

        for r, c in possible_targets:
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if (r, c) not in player_board.attacked_cells:
                    self.target_queue.append((r, c))

    def find_direction(self):
        """
        Determine whether the current ship is horizontal or vertical.
        """
        first_row, first_col = self.hit_stack[0]
        second_row, second_col = self.hit_stack[1]

        if first_row == second_row:
            self.direction = "H"
        elif first_col == second_col:
            self.direction = "V"

    def add_line_targets(self, player_board):
        """
        Once direction is known, keep attacking in that straight line.

        Args:
            player_board (Board): The player's board.
        """
        rows = [cell[0] for cell in self.hit_stack]
        cols = [cell[1] for cell in self.hit_stack]

        self.target_queue = []

        if self.direction == "H":
            row = rows[0]
            left_col = min(cols) - 1
            right_col = max(cols) + 1

            possible_targets = [
                (row, left_col),
                (row, right_col)
            ]

        elif self.direction == "V":
            col = cols[0]
            top_row = min(rows) - 1
            bottom_row = max(rows) + 1

            possible_targets = [
                (top_row, col),
                (bottom_row, col)
            ]

        else:
            possible_targets = []

        for r, c in possible_targets:
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if (r, c) not in player_board.attacked_cells:
                    self.target_queue.append((r, c))
