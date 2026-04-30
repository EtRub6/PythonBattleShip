# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

"""
settings.py

This file stores constants used by the Battleship game.
Keeping these values in one place makes the rest of the code cleaner.
"""

# Grid and cell sizing
GRID_SIZE = 10
CELL_SIZE = 30
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE

# Margins for spacing the boards and text on the screen
MARGIN = 40
TOP_MARGIN = 90
BOTTOM_MARGIN = 70

# Total screen dimensions
WIDTH = BOARD_WIDTH * 2 + MARGIN * 4 + 160
HEIGHT = BOARD_HEIGHT + TOP_MARGIN + BOTTOM_MARGIN

# RGB color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 82, 184)
GRAY = (180, 180, 180)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
NAVY = (20, 40, 90)
YELLOW = (255, 215, 0)

# X and Y offsets for where each board begins on the screen
PLAYER_OFFSET_X = MARGIN
ENEMY_OFFSET_X = MARGIN * 2 + BOARD_WIDTH
BOARD_OFFSET_Y = TOP_MARGIN

# List of ship sizes for both fleets
SHIP_SIZES = [4, 3, 3, 2, 2, 1, 1, 1]

# Frame rate
FPS = 30
