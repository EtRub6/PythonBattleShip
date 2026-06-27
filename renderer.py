# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

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
    BLUE,
    GRAY,
    RED,
    GREEN,
    NAVY,
    YELLOW,
    PLAYER_OFFSET_X,
    ENEMY_OFFSET_X,
    BOARD_OFFSET_Y,
)


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

    def draw_menu(self, game):
        """
        Draw the start menu screen.

        Args:
            game (Game): The current game object.
        """
        self.screen.fill(BLUE)

        big_font = self.fonts["big_font"]
        font = self.fonts["font"]
        small_font = self.fonts["small_font"]

        title = big_font.render("Battleship", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 115))
        self.screen.blit(title, title_rect)

        score_text = font.render(
            f"Your Wins: {game.player_wins}   Enemy Wins: {game.enemy_wins}",
            True,
            WHITE
        )
        score_rect = score_text.get_rect(center=(WIDTH // 2, 180))
        self.screen.blit(score_text, score_rect)

        message_text = small_font.render(game.message, True, YELLOW)
        # Draw this higher so it does not overlap the Play button.
        message_rect = message_text.get_rect(center=(WIDTH // 2, 220))
        self.screen.blit(message_text, message_rect)

        play_button = game.get_play_button_rect()

        pygame.draw.rect(self.screen, GREEN, play_button)
        pygame.draw.rect(self.screen, WHITE, play_button, 2)

        play_text = font.render("Play", True, WHITE)
        play_rect = play_text.get_rect(center=play_button.center)
        self.screen.blit(play_text, play_rect)

        pygame.display.flip()

    def draw_grid(self, offset_x, offset_y):
        """
        Draw the grid outline at the given location.

        Args:
            offset_x (int): X position of the board.
            offset_y (int): Y position of the board.
        """
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = offset_x + col * CELL_SIZE
                y = offset_y + row * CELL_SIZE
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def draw_board(self, board, offset_x, offset_y, reveal_ships=False):
        """
        Draw a board and its visible symbols.

        Args:
            board (Board): The board to draw.
            offset_x (int): X position of the board.
            offset_y (int): Y position of the board.
            reveal_ships (bool): Whether ships should be visible.
        """
        font = self.fonts["font"]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = offset_x + col * CELL_SIZE
                y = offset_y + row * CELL_SIZE

                pygame.draw.rect(self.screen, NAVY, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

                cell_value = board.grid[row][col]

                # Hide ships on the enemy board.
                if cell_value == 'S' and not reveal_ships:
                    cell_value = ' '

                if cell_value != ' ':
                    color = WHITE

                    if cell_value == 'X':
                        color = RED
                    elif cell_value == 'S':
                        color = GREEN

                    text = font.render(cell_value, True, color)
                    text_rect = text.get_rect(
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                    )
                    self.screen.blit(text, text_rect)

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

        color = GREEN if valid else RED

        for r, c in ship_cells:
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                x = PLAYER_OFFSET_X + c * CELL_SIZE
                y = BOARD_OFFSET_Y + r * CELL_SIZE
                pygame.draw.rect(
                    self.screen,
                    color,
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
        message_surface = small_font.render(game.message, True, YELLOW)

        self.screen.blit(instruction_surface, (MARGIN, HEIGHT - 55))
        self.screen.blit(message_surface, (MARGIN, HEIGHT - 30))

    def draw_game_over_panel(self, game):
        """
        Draw a game-over message on top of the boards.

        This keeps the Battleship screen visible, but shows whether
        the player won or lost and gives a button to return to menu.
        """
        big_font = self.fonts["big_font"]
        font = self.fonts["font"]
        small_font = self.fonts["small_font"]

        # Semi-simple panel drawn over the board area.
        panel_rect = pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 - 105, 420, 210)
        pygame.draw.rect(self.screen, BLUE, panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 3)

        if game.winner == "player":
            main_text = "You Won!"
            color = GREEN
        else:
            main_text = "You Lost!"
            color = RED

        title = big_font.render(main_text, True, color)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        self.screen.blit(title, title_rect)

        score_text = small_font.render(
            f"Your Wins: {game.player_wins}   Enemy Wins: {game.enemy_wins}",
            True,
            WHITE
        )
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15))
        self.screen.blit(score_text, score_rect)

        prompt = small_font.render("Go back to menu to start another game?", True, YELLOW)
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(prompt, prompt_rect)

        menu_button = game.get_menu_button_rect()
        pygame.draw.rect(self.screen, GREEN, menu_button)
        pygame.draw.rect(self.screen, WHITE, menu_button, 2)

        button_text = font.render("Menu", True, WHITE)
        button_rect = button_text.get_rect(center=menu_button.center)
        self.screen.blit(button_text, button_rect)


    def draw_ship_status(self, game):
        """
        Draw enemy fleet tracker on right side.
        """
        small_font = self.fonts["small_font"]
        x = ENEMY_OFFSET_X + BOARD_WIDTH + 20
        y = BOARD_OFFSET_Y

        title = small_font.render("Enemy Fleet", True, WHITE)
        self.screen.blit(title, (x, y))
        y += 35

        for ship in game.enemy.board.ships:
            if ship.is_sunk():
                status = f"Size {ship.size}: Sunk"
                color = RED
            else:
                status = f"Size {ship.size}: Alive"
                color = GREEN

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

        self.screen.fill(BLUE)

        self.draw_labels(game)

        self.draw_grid(PLAYER_OFFSET_X, BOARD_OFFSET_Y)
        self.draw_grid(ENEMY_OFFSET_X, BOARD_OFFSET_Y)

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

        self.draw_ship_status(game)

        self.draw_hover_ship_preview(game)

        if game.phase == "game_over":
            self.draw_game_over_panel(game)

        pygame.display.flip()
