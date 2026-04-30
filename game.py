# Authors: Ethan Rubinstein, Nolan Duarte, Freddy Ngufy

"""
game.py

This file contains the Game class.
The Game class controls the overall game flow.
"""

import pygame
import sys

from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    CELL_SIZE,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    PLAYER_OFFSET_X,
    ENEMY_OFFSET_X,
    BOARD_OFFSET_Y,
    SHIP_SIZES,
)

from player import Player
from enemy import Enemy
from renderer import Renderer
from sound_manager import SoundManager


class Game:
    """
    Controls the Battleship game.
    """

    def __init__(self):
        """
        Create and initialize the full game.
        """
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleship")
        self.clock = pygame.time.Clock()

        self.fonts = {
            "font": pygame.font.Font(None, 32),
            "small_font": pygame.font.Font(None, 24),
            "big_font": pygame.font.Font(None, 56),
        }

        self.renderer = Renderer(self.screen, self.fonts)

        # Sound manager handles music and sound effects.
        self.sound_manager = SoundManager()
        self.sound_manager.play_music("TitleScreen.mp3", loop=True)

        # Score counters stay alive even after starting a new game.
        self.player_wins = 0
        self.enemy_wins = 0

        # Tracks how many of the player's ships the enemy has sunk.
        self.player_ships_destroyed = 0

        # Create players and boards.
        self.player = Player("Player")
        self.enemy = Enemy("Enemy")

        self.ship_sizes = SHIP_SIZES
        self.current_ship_index = 0
        self.orientation = "H"

        # The game starts at the menu.
        self.phase = "menu"

        self.player_turn = True
        self.winner = None
        self.message = "Click Play to start."

        self.enemy_attack_start_time = None

    def get_play_button_rect(self):
        """
        Get the rectangle for the Play button.

        Returns:
            pygame.Rect: Rectangle used for drawing and clicking the button.
        """
        return pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 45, 160, 50)

    def start_new_game(self):
        """
        Reset the boards and start a new game.

        This does not reset the win counters.
        """
        self.player = Player("Player")
        self.enemy = Enemy("Enemy")

        # Enemy ships follow the same no-touching placement rule.
        self.enemy.board.place_random_fleet()

        self.current_ship_index = 0
        self.orientation = "H"

        self.phase = "placement"
        self.player_turn = True
        self.winner = None

        # Reset destroyed ship counter each new game.
        self.player_ships_destroyed = 0

        self.message = "Place your ships. Ships cannot touch."

        # Start level music when a new game begins.
        self.sound_manager.play_music("Level1.mp3", loop=True)

    def handle_menu_click(self, mouse_x, mouse_y):
        """
        Handle mouse clicks on the menu screen.

        Args:
            mouse_x (int): Mouse x-position.
            mouse_y (int): Mouse y-position.
        """
        play_button = self.get_play_button_rect()

        if play_button.collidepoint(mouse_x, mouse_y):
            self.sound_manager.play_sound("click")
            self.start_new_game()

    def get_menu_button_rect(self):
        """
        Get the rectangle for the Menu button on the game-over screen.

        Returns:
            pygame.Rect: Rectangle used for drawing and clicking the button.
        """
        return pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 55, 160, 50)

    def handle_game_over_click(self, mouse_x, mouse_y):
        """
        Handle mouse clicks on the game-over screen.

        Args:
            mouse_x (int): Mouse x-position.
            mouse_y (int): Mouse y-position.
        """
        menu_button = self.get_menu_button_rect()

        if menu_button.collidepoint(mouse_x, mouse_y):
            self.sound_manager.play_sound("click")
            self.phase = "menu"
            self.sound_manager.play_music("TitleScreen.mp3", loop=True)

            if self.winner == "player":
                self.message = f"You won! Your total wins: {self.player_wins}"
            else:
                self.message = f"Enemy won. Your wins: {self.player_wins}"

    def handle_placement_click(self, mouse_x, mouse_y):
        """
        Handle mouse clicks during ship placement.

        Args:
            mouse_x (int): Mouse x-position.
            mouse_y (int): Mouse y-position.
        """
        board_left = PLAYER_OFFSET_X
        board_right = PLAYER_OFFSET_X + BOARD_WIDTH
        board_top = BOARD_OFFSET_Y
        board_bottom = BOARD_OFFSET_Y + BOARD_HEIGHT

        if not (board_left <= mouse_x < board_right and board_top <= mouse_y < board_bottom):
            return

        col = (mouse_x - PLAYER_OFFSET_X) // CELL_SIZE
        row = (mouse_y - BOARD_OFFSET_Y) // CELL_SIZE

        if self.current_ship_index >= len(self.ship_sizes):
            return

        size = self.ship_sizes[self.current_ship_index]

        placed = self.player.board.place_ship(size, row, col, self.orientation)

        if placed:
            self.current_ship_index += 1

            if self.current_ship_index >= len(self.ship_sizes):
                self.phase = "battle"
                self.message = "Battle started! Your turn."
            else:
                next_size = self.ship_sizes[self.current_ship_index]
                self.message = f"Placed ship. Place ship of size {next_size}."
        else:
            self.message = "Invalid placement. Ships cannot touch."

    def handle_player_attack(self, mouse_x, mouse_y):
        """
        Handle the player's attack on the enemy board.

        Args:
            mouse_x (int): Mouse x-position.
            mouse_y (int): Mouse y-position.
        """
        if not self.player_turn:
            return

        board_left = ENEMY_OFFSET_X
        board_right = ENEMY_OFFSET_X + BOARD_WIDTH
        board_top = BOARD_OFFSET_Y
        board_bottom = BOARD_OFFSET_Y + BOARD_HEIGHT

        if not (board_left <= mouse_x < board_right and board_top <= mouse_y < board_bottom):
            return

        col = (mouse_x - ENEMY_OFFSET_X) // CELL_SIZE
        row = (mouse_y - BOARD_OFFSET_Y) // CELL_SIZE

        result, ship = self.player.attack(self.enemy.board, row, col)

        if result == "repeat":
            self.message = "You cannot attack that square."
            return

        elif result == "hit":
            self.message = "Hit!"
            self.sound_manager.play_sound("hit")
            self.player_turn = True

        elif result == "sunk":
            self.message = f"You sunk an enemy ship of size {ship.size}!"
            self.sound_manager.play_sound("sunk")

        else:
            self.message = "Miss."
            self.sound_manager.play_sound("miss")
            self.player_turn = False
            self.enemy_attack_start_time = pygame.time.get_ticks()

        if self.enemy.board.all_ships_sunk():
            self.player_wins += 1
            self.winner = "player"
            self.phase = "game_over"
            self.message = "You won! Click Menu to play again."
            self.sound_manager.play_music("Victory.mp3", loop=False)
            return




    def enemy_attack(self):
        """
        Perform the enemy's turn.
        """
        if self.phase != "battle" or self.player_turn:
            return

        # Enemy chooses where to attack.
        row, col = self.enemy.choose_attack(self.player.board)

        # Enemy attacks the player's board.
        result, ship = self.enemy.attack(self.player.board, row, col)

        # Enemy updates its AI memory based on the result.
        self.enemy.process_attack_result(row, col, result, self.player.board)

        if result == "hit":
            self.message = f"Enemy hit your ship at ({row}, {col})!"
            self.sound_manager.play_sound("hit")
            self.player_turn = False
            self.enemy_attack_start_time = pygame.time.get_ticks()

        elif result == "sunk":
            self.message = f"Enemy sunk your ship of size {ship.size}!"
            self.sound_manager.play_sound("sunk")

            self.player_ships_destroyed += 1

            # Increase music intensity as the player loses ships
            if self.player_ships_destroyed == 1:
                self.sound_manager.play_music("Level2.mp3", loop=True)

            elif self.player_ships_destroyed == 2:
                self.sound_manager.play_music("Level3.mp3", loop=True)

            self.enemy_attack_start_time = pygame.time.get_ticks()

        elif result == "miss":
            self.message = f"Enemy missed at ({row}, {col})."
            self.sound_manager.play_sound("miss")
            self.player_turn = True
            self.enemy_attack_start_time = None

        if self.player.board.all_ships_sunk():
            self.enemy_wins += 1
            self.winner = "enemy"
            self.phase = "game_over"
            self.message = "You lost. Click Menu to try again."
            self.sound_manager.play_music("game_over.mp3", loop=False)
            return



    def handle_events(self):
        """
        Process all pygame events.

        Handles:
            - closing the window
            - pressing R to rotate ships
            - mouse clicks for menu, placement, and attacks
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.phase == "placement" and event.key == pygame.K_r:
                    if self.orientation == "H":
                        self.orientation = "V"
                    else:
                        self.orientation = "H"

                    self.message = f"Orientation changed to {self.orientation}."

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if self.phase == "menu":
                    self.handle_menu_click(x, y)

                elif self.phase == "placement":
                    self.handle_placement_click(x, y)

                elif self.phase == "battle":
                    self.handle_player_attack(x, y)

                elif self.phase == "game_over":
                    self.handle_game_over_click(x, y)

    def run(self):
        """
        Main game loop.

        Repeatedly:
            - handles input
            - lets the enemy move when needed
            - draws the screen
            - limits frame rate
        """
        running = True

        while running:
            self.handle_events()

            if self.phase == "battle" and not self.player_turn:
                current_time = pygame.time.get_ticks()

                if self.enemy_attack_start_time is not None:
                    if current_time - self.enemy_attack_start_time >= 1000:
                        self.enemy_attack()

            self.renderer.draw_all(self)
            self.clock.tick(FPS)
