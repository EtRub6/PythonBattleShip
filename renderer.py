# Author: Ethan Rubinstein

"""
renderer.py

This file contains the Renderer class.
The Renderer is responsible only for drawing things on the screen.
"""

import pygame
from settings import (
    GRID_SIZE,
    CELL_SIZE,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    MARGIN,
    HEIGHT,
    WIDTH,
    WHITE,
    PLAYER_OFFSET_X,
    ENEMY_OFFSET_X,
    BOARD_OFFSET_Y,
    OCEAN_TOP,
    OCEAN_BOTTOM,
    WATER_DARK,
    WATER_LIGHT,
    GRID_LINE,
    BOARD_FRAME,
    SHIP_HULL,
    SHIP_HULL_HIT,
    SHIP_OUTLINE,
    HIT_RED,
    HIT_BURST,
    MISS_SPLASH,
    MISS_RING,
    GOLD,
    BTN_GREEN,
    BTN_GREEN_HOVER,
    BTN_BORDER,
    PANEL_BG,
    PANEL_BORDER,
    OVERLAY_DIM,
    BORDER_RADIUS,
)

COLUMN_LABELS = "ABCDEFGHIJ"


class Renderer:
    """
    Handles all drawing for the Battleship game.
    """

    def __init__(self, screen, fonts):
        """
        Create a renderer.

        Args:
            screen: The pygame display surface.
            fonts (dict): Dictionary of pygame font objects.
        """
        self.screen = screen
        self.fonts = fonts
        self.background = self._build_ocean_background()

    def _build_ocean_background(self):
        """
        Pre-render a vertical ocean gradient once, instead of filling a
        flat color every frame. Cheap to blit, and looks a lot less flat.

        Returns:
            pygame.Surface: A WIDTH x HEIGHT gradient background.
        """
        background = pygame.Surface((WIDTH, HEIGHT))

        for y in range(HEIGHT):
            t = y / max(HEIGHT - 1, 1)
            r = OCEAN_TOP[0] + (OCEAN_BOTTOM[0] - OCEAN_TOP[0]) * t
            g = OCEAN_TOP[1] + (OCEAN_BOTTOM[1] - OCEAN_TOP[1]) * t
            b = OCEAN_TOP[2] + (OCEAN_BOTTOM[2] - OCEAN_TOP[2]) * t
            pygame.draw.line(background, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

        return background

    def draw_text_with_shadow(self, font, text, color, center, shadow_offset=3):
        """
        Render text twice — a dark shadow copy offset slightly, then the
        real text on top — so titles stand out against the background.

        Args:
            font: The pygame font to render with.
            text (str): The text to draw.
            color (tuple): RGB color of the main text.
            center (tuple): (x, y) center position on screen.
            shadow_offset (int): How many pixels to offset the shadow.
        """
        shadow = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(
            center=(center[0] + shadow_offset, center[1] + shadow_offset)
        )
        self.screen.blit(shadow, shadow_rect)

        main = font.render(text, True, color)
        main_rect = main.get_rect(center=center)
        self.screen.blit(main, main_rect)

    def draw_button(self, rect, label, hint=None):
        """
        Draw a rounded, drop-shadowed button that lights up on hover.

        Args:
            rect (pygame.Rect): The button's position and size.
            label (str): Main button text.
            hint (str): Optional smaller line of text below the button.
        """
        font = self.fonts["font"]
        small_font = self.fonts["small_font"]

        hovered = rect.collidepoint(pygame.mouse.get_pos())
        fill_color = BTN_GREEN_HOVER if hovered else BTN_GREEN

        shadow_rect = rect.move(0, 4)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.screen, fill_color, rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.screen, BTN_BORDER, rect, 2, border_radius=BORDER_RADIUS)

        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

        if hint is not None:
            hint_surface = small_font.render(hint, True, WHITE)
            hint_rect = hint_surface.get_rect(midtop=(rect.centerx, rect.bottom + 6))
            self.screen.blit(hint_surface, hint_rect)

    def draw_menu(self, game):
        """
        Draw the start menu screen.

        Args:
            game (Game): The current game object.
        """
        self.screen.blit(self.background, (0, 0))

        big_font = self.fonts["big_font"]
        font = self.fonts["font"]
        small_font = self.fonts["small_font"]

        self.draw_text_with_shadow(big_font, "Battleship", WHITE, (WIDTH // 2, 115))

        score_text = font.render(
            f"Your Wins: {game.player_wins}   Enemy Wins: {game.enemy_wins}",
            True,
            WHITE
        )
        score_rect = score_text.get_rect(center=(WIDTH // 2, 180))
        self.screen.blit(score_text, score_rect)

        message_text = small_font.render(game.message, True, GOLD)
        # Draw this higher so it does not overlap the Play button.
        message_rect = message_text.get_rect(center=(WIDTH // 2, 220))
        self.screen.blit(message_text, message_rect)

        self.draw_button(game.get_play_button_rect(), "Play")

        pygame.display.flip()

    def draw_board_frame(self, offset_x, offset_y):
        """
        Draw a decorative frame around a board.

        Args:
            offset_x (int): X position of the board.
            offset_y (int): Y position of the board.
        """
        frame_rect = pygame.Rect(
            offset_x - 3, offset_y - 3, BOARD_WIDTH + 6, BOARD_HEIGHT + 6
        )
        pygame.draw.rect(self.screen, BOARD_FRAME, frame_rect, 3, border_radius=4)

    def draw_board_coordinates(self, offset_x, offset_y):
        """
        Draw column letters (A-J) above and row numbers (1-10) beside
        a board, the way a real Battleship grid is labeled.

        Args:
            offset_x (int): X position of the board.
            offset_y (int): Y position of the board.
        """
        small_font = self.fonts["small_font"]

        for col in range(GRID_SIZE):
            label = small_font.render(COLUMN_LABELS[col], True, WHITE)
            x = offset_x + col * CELL_SIZE + CELL_SIZE // 2
            label_rect = label.get_rect(midbottom=(x, offset_y - 4))
            self.screen.blit(label, label_rect)

        for row in range(GRID_SIZE):
            label = small_font.render(str(row + 1), True, WHITE)
            y = offset_y + row * CELL_SIZE + CELL_SIZE // 2
            label_rect = label.get_rect(midright=(offset_x - 6, y))
            self.screen.blit(label, label_rect)

    def _draw_hit_marker(self, x, y):
        """
        Draw a hit as a warm burst with a bold X on top.

        Args:
            x (int): Left edge of the cell in screen coordinates.
            y (int): Top edge of the cell in screen coordinates.
        """
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        pygame.draw.circle(self.screen, HIT_BURST, center, CELL_SIZE // 2 - 3)
        pygame.draw.circle(self.screen, HIT_RED, center, CELL_SIZE // 2 - 3, 2)

        pad = 8
        pygame.draw.line(self.screen, WHITE, (x + pad, y + pad),
                          (x + CELL_SIZE - pad, y + CELL_SIZE - pad), 3)
        pygame.draw.line(self.screen, WHITE, (x + CELL_SIZE - pad, y + pad),
                          (x + pad, y + CELL_SIZE - pad), 3)

    def _draw_miss_marker(self, x, y):
        """
        Draw a miss as a pale splash circle.

        Args:
            x (int): Left edge of the cell in screen coordinates.
            y (int): Top edge of the cell in screen coordinates.
        """
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        pygame.draw.circle(self.screen, MISS_SPLASH, center, CELL_SIZE // 4)
        pygame.draw.circle(self.screen, MISS_RING, center, CELL_SIZE // 4, 2)

    def _draw_ship_hull(self, ship, offset_x, offset_y):
        """
        Draw one ship as a single rounded hull spanning all of its
        cells, instead of a letter repeated in every cell it occupies.

        Args:
            ship (Ship): The ship to draw.
            offset_x (int): X position of the board.
            offset_y (int): Y position of the board.
        """
        rows = [cell[0] for cell in ship.cells]
        cols = [cell[1] for cell in ship.cells]

        left = offset_x + min(cols) * CELL_SIZE
        top = offset_y + min(rows) * CELL_SIZE
        width = (max(cols) - min(cols) + 1) * CELL_SIZE
        height = (max(rows) - min(rows) + 1) * CELL_SIZE

        pad = 4
        hull_rect = pygame.Rect(left + pad, top + pad, width - pad * 2, height - pad * 2)

        color = SHIP_HULL_HIT if ship.is_sunk() else SHIP_HULL
        pygame.draw.rect(self.screen, color, hull_rect, border_radius=6)
        pygame.draw.rect(self.screen, SHIP_OUTLINE, hull_rect, 2, border_radius=6)

    def draw_board(self, board, offset_x, offset_y, reveal_ships=False):
        """
        Draw a board and its visible symbols.

        Args:
            board (Board): The board to draw.
            offset_x (int): X position of the board.
            offset_y (int): Y position of the board.
            reveal_ships (bool): Whether ships should be visible.
        """
        # Pass 1: water tiles, alternating shades for a subtle checker pattern.
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = offset_x + col * CELL_SIZE
                y = offset_y + row * CELL_SIZE

                water_color = WATER_LIGHT if (row + col) % 2 == 0 else WATER_DARK
                pygame.draw.rect(self.screen, water_color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, GRID_LINE, (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Pass 2: ship hulls, drawn as one shape per ship, under the hit/miss marks.
        if reveal_ships:
            for ship in board.ships:
                self._draw_ship_hull(ship, offset_x, offset_y)

        # Pass 3: hit and miss marks on top of everything else.
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_value = board.grid[row][col]

                if cell_value not in ('X', 'O'):
                    continue

                x = offset_x + col * CELL_SIZE
                y = offset_y + row * CELL_SIZE

                if cell_value == 'X':
                    self._draw_hit_marker(x, y)
                else:
                    self._draw_miss_marker(x, y)

    def draw_hover_ship_preview(self, game):
        """
        Draw a temporary ship preview during placement.

        Green means valid placement.
        Red means invalid placement.

        Args:
            game (Game): The current game object.
        """
        if game.phase != "placement":
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()

        board_left = PLAYER_OFFSET_X
        board_right = PLAYER_OFFSET_X + BOARD_WIDTH
        board_top = BOARD_OFFSET_Y
        board_bottom = BOARD_OFFSET_Y + BOARD_HEIGHT

        if not (board_left <= mouse_x < board_right and board_top <= mouse_y < board_bottom):
            return

        col = (mouse_x - PLAYER_OFFSET_X) // CELL_SIZE
        row = (mouse_y - BOARD_OFFSET_Y) // CELL_SIZE

        if game.current_ship_index >= len(game.ship_sizes):
            return

        size = game.ship_sizes[game.current_ship_index]
        ship_cells = game.player.board.get_ship_cells(row, col, size, game.orientation)
        valid = game.player.board.can_place_ship(ship_cells)

        fill_color = (60, 210, 130, 110) if valid else (230, 70, 70, 110)
        outline_color = (60, 210, 130) if valid else (230, 70, 70)

        overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        overlay.fill(fill_color)

        for r, c in ship_cells:
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                x = PLAYER_OFFSET_X + c * CELL_SIZE
                y = BOARD_OFFSET_Y + r * CELL_SIZE
                self.screen.blit(overlay, (x, y))
                pygame.draw.rect(
                    self.screen,
                    outline_color,
                    (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
                    2
                )

    def draw_random_button(self, game):
        """
        Draw the "Randomize Ships" button during the placement phase.

        Args:
            game (Game): The current game object.
        """
        if game.phase != "placement":
            return

        self.draw_button(game.get_random_button_rect(), "Randomize", "Auto-place & start")

    def draw_hover_attack_highlight(self, game):
        """
        Highlight the enemy cell under the mouse during battle, so the
        player can see exactly which square they are about to attack.

        A thin crosshair runs the full length of the cell's row and
        column, with a bordered highlight on the exact cell.

        Args:
            game (Game): The current game object.
        """
        if game.phase != "battle" or not game.player_turn:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()

        board_left = ENEMY_OFFSET_X
        board_right = ENEMY_OFFSET_X + BOARD_WIDTH
        board_top = BOARD_OFFSET_Y
        board_bottom = BOARD_OFFSET_Y + BOARD_HEIGHT

        if not (board_left <= mouse_x < board_right and board_top <= mouse_y < board_bottom):
            return

        col = (mouse_x - ENEMY_OFFSET_X) // CELL_SIZE
        row = (mouse_y - BOARD_OFFSET_Y) // CELL_SIZE

        if (row, col) in game.enemy.board.attacked_cells:
            return

        x = ENEMY_OFFSET_X + col * CELL_SIZE
        y = BOARD_OFFSET_Y + row * CELL_SIZE

        row_y = y + CELL_SIZE // 2
        col_x = x + CELL_SIZE // 2
        pygame.draw.line(self.screen, GOLD, (board_left, row_y), (board_right, row_y), 1)
        pygame.draw.line(self.screen, GOLD, (col_x, board_top), (col_x, board_bottom), 1)

        pygame.draw.rect(
            self.screen,
            GOLD,
            (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
            2
        )

    def draw_labels(self, game):
        """
        Draw board labels, instructions, and game messages.

        Args:
            game (Game): The current game object.
        """
        font = self.fonts["font"]
        small_font = self.fonts["small_font"]

        player_label = font.render("Player Board", True, WHITE)
        enemy_label = font.render("Enemy Board", True, WHITE)

        self.screen.blit(player_label, (PLAYER_OFFSET_X + 70, 25))
        self.screen.blit(enemy_label, (ENEMY_OFFSET_X + 70, 25))

        if game.phase == "placement":
            if game.current_ship_index < len(game.ship_sizes):
                size = game.ship_sizes[game.current_ship_index]
                instruction = (
                    f"Place ship size {size} | Press R to rotate | "
                    f"Orientation: {game.orientation}"
                )
            else:
                instruction = "Preparing battle..."
        elif game.phase == "battle":
            turn_text = "Your turn" if game.player_turn else "Enemy turn"
            instruction = f"{turn_text} | X = hit, O = miss"
        else:
            instruction = "Game over"

        instruction_surface = small_font.render(instruction, True, WHITE)
        message_surface = small_font.render(game.message, True, GOLD)

        self.screen.blit(instruction_surface, (MARGIN, HEIGHT - 55))
        self.screen.blit(message_surface, (MARGIN, HEIGHT - 30))

    def draw_game_over_panel(self, game):
        """
        Draw a game-over message on top of the boards.

        This keeps the Battleship screen visible (dimmed), but shows
        whether the player won or lost and gives a button to return
        to the menu.
        """
        big_font = self.fonts["big_font"]
        small_font = self.fonts["small_font"]

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((OVERLAY_DIM[0], OVERLAY_DIM[1], OVERLAY_DIM[2], 150))
        self.screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 - 105, 420, 210)
        shadow_rect = panel_rect.move(0, 5)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.screen, PANEL_BORDER, panel_rect, 3, border_radius=BORDER_RADIUS)

        if game.winner == "player":
            main_text = "You Won!"
            color = (76, 217, 123)
        else:
            main_text = "You Lost!"
            color = HIT_RED

        self.draw_text_with_shadow(
            big_font, main_text, color, (WIDTH // 2, HEIGHT // 2 - 60)
        )

        score_text = small_font.render(
            f"Your Wins: {game.player_wins}   Enemy Wins: {game.enemy_wins}",
            True,
            WHITE
        )
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15))
        self.screen.blit(score_text, score_rect)

        prompt = small_font.render("Go back to menu to start another game?", True, GOLD)
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(prompt, prompt_rect)

        self.draw_button(game.get_menu_button_rect(), "Menu")

    def draw_ship_status(self, game):
        """
        Draw enemy fleet tracker on right side.

        Only shown once the battle has started (or ended) — during
        placement this space is used by the Randomize button instead.
        """
        if game.phase not in ("battle", "game_over"):
            return

        small_font = self.fonts["small_font"]
        x = ENEMY_OFFSET_X + BOARD_WIDTH + 20
        y = BOARD_OFFSET_Y

        title = small_font.render("Enemy Fleet", True, GOLD)
        self.screen.blit(title, (x, y))
        y += 35

        for ship in game.enemy.board.ships:
            if ship.is_sunk():
                status = f"Size {ship.size}: Sunk"
                color = HIT_RED
            else:
                status = f"Size {ship.size}: Alive"
                color = (110, 220, 150)

            text = small_font.render(status, True, color)
            self.screen.blit(text, (x, y))
            y += 28

    def draw_all(self, game):
        """
        Draw the whole game screen.

        Args:
            game (Game): The current game object.
        """
        if game.phase == "menu":
            self.draw_menu(game)
            return

        self.screen.blit(self.background, (0, 0))

        self.draw_labels(game)

        self.draw_board_coordinates(PLAYER_OFFSET_X, BOARD_OFFSET_Y)
        self.draw_board_coordinates(ENEMY_OFFSET_X, BOARD_OFFSET_Y)

        self.draw_board(
            game.player.board,
            PLAYER_OFFSET_X,
            BOARD_OFFSET_Y,
            reveal_ships=True
        )

        self.draw_board(
            game.enemy.board,
            ENEMY_OFFSET_X,
            BOARD_OFFSET_Y,
            reveal_ships=False
        )

        self.draw_board_frame(PLAYER_OFFSET_X, BOARD_OFFSET_Y)
        self.draw_board_frame(ENEMY_OFFSET_X, BOARD_OFFSET_Y)

        self.draw_ship_status(game)

        self.draw_hover_ship_preview(game)
        self.draw_hover_attack_highlight(game)
        self.draw_random_button(game)

        if game.phase == "game_over":
            self.draw_game_over_panel(game)

        pygame.display.flip()
