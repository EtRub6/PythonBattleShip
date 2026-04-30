# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

"""
main.py

This is the file you run to start the Battleship game.
"""

from game import Game


def main():
    """
    Create the game object and start the game loop.
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
