# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

"""
player.py

This file contains the Player class.
A Player has a name and a board.
"""

from board import Board


class Player:
    """
    Represents a human player.
    """

    def __init__(self, name):
        """
        Create a player.

        Args:
            name (str): Name of the player.
        """
        self.name = name
        self.board = Board()

    def attack(self, enemy_board, row, col):
        """
        Attack another player's board.

        Args:
            enemy_board (Board): The board being attacked.
            row (int): Row to attack.
            col (int): Column to attack.

        Returns:
            tuple: The attack result and the affected ship.
        """
        return enemy_board.receive_attack(row, col)
