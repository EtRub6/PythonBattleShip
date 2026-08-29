# Author: Ethan Rubinstein

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

# --- Extended nautical palette used by the renderer ---

# Background gradient: deep water at the bottom, lighter water up top.
OCEAN_TOP = (26, 71, 128)
OCEAN_BOTTOM = (8, 22, 46)

# Board cell "water" — two close shades give a subtle checkerboard texture.
WATER_DARK = (15, 38, 74)
WATER_LIGHT = (21, 47, 86)
GRID_LINE = (68, 102, 142)
BOARD_FRAME = (120, 160, 200)

# Ships are drawn as one hull shape spanning their cells, not per-cell letters.
SHIP_HULL = (150, 158, 168)
SHIP_HULL_HIT = (100, 84, 84)
SHIP_OUTLINE = (55, 61, 70)

# Hits: a warm burst under a bold X. Misses: a pale splash circle.
HIT_RED = (233, 69, 56)
HIT_BURST = (255, 148, 64)
MISS_SPLASH = (206, 227, 242)
MISS_RING = (120, 158, 190)

# Gold accent used for messages, highlights, and titles.
GOLD = (255, 197, 61)

# Buttons
BTN_GREEN = (37, 168, 93)
BTN_GREEN_HOVER = (58, 196, 118)
BTN_BORDER = (232, 245, 238)

# Panels (game-over dialog, text backing) and the dimming overlay behind them.
PANEL_BG = (13, 30, 56)
PANEL_BORDER = GOLD
OVERLAY_DIM = (0, 0, 0)

# Corner rounding used across buttons and panels.
BORDER_RADIUS = 10

# X and Y offsets for where each board begins on the screen
PLAYER_OFFSET_X = MARGIN
ENEMY_OFFSET_X = MARGIN * 2 + BOARD_WIDTH
BOARD_OFFSET_Y = TOP_MARGIN

# List of ship sizes for both fleets
SHIP_SIZES = [4, 3, 3, 2, 2, 1, 1, 1]

# Frame rate
FPS = 30
