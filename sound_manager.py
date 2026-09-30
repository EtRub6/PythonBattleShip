# Author: Ethan Rubinstein


"""
sound_manager.py

This file contains the SoundManager class.
It handles music and sound effects using pygame.mixer.
"""

import os
import pygame


class SoundManager:
    """
    Handles background music and sound effects.
    """

    def __init__(self):
        """
        Initialize the mixer and load sound effects.
        """
        # Build the sounds folder path relative to this file, not the
        # current working directory. This way the game finds its audio
        # files no matter where it's launched from.
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sound_folder = os.path.join(base_dir, "sounds")

        # Store which background song is currently playing.
        self.current_music = None

        # Mute state and normal music volume.
        self.muted = False
        self.music_volume = 0.3

        # Try to initialize pygame's sound system.
        # If sound fails, the game will still run.
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except pygame.error:
            self.sound_enabled = False

        self.sounds = {}

        if self.sound_enabled:
            self.load_sounds()

    def get_sound_path(self, filename):
        """
        Build a path to a file inside the sounds folder.

        Args:
            filename (str): Name of the sound file.

        Returns:
            str: Full sound path.
        """
        return os.path.join(self.sound_folder, filename)

    def load_sounds(self):
        """
        Load short sound effects.
        """
        self.sounds["hit"] = self.load_sound("explosion.mp3")
        self.sounds["miss"] = self.load_sound("watersplash2.mp3")
        self.sounds["sunk"] = self.load_sound("DeathFlash.mp3")
        self.sounds["click"] = self.load_sound("sonar_ping.mp3")

    def load_sound(self, filename):
        """
        Safely load one sound effect.

        Args:
            filename (str): File name inside the sounds folder.

        Returns:
            pygame.mixer.Sound or None
        """
        path = self.get_sound_path(filename)

        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            return None
        except FileNotFoundError:
            return None

    def play_sound(self, sound_name):
        """
        Play one sound effect.

        Args:
            sound_name (str): Name of the sound effect.
        """
        if not self.sound_enabled or self.muted:
            return

        sound = self.sounds.get(sound_name)

        if sound is not None:
            sound.play()

    def toggle_mute(self):
        """
        Mute or unmute all music and sound effects.
        """
        self.muted = not self.muted

        if not self.sound_enabled:
            return

        if self.muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.music_volume)

    def play_music(self, filename, loop=True):
        """
        Play background music.

        Args:
            filename (str): Music file inside the sounds folder.
            loop (bool): Whether the music should loop.
        """
        if not self.sound_enabled:
            return

        if self.current_music == filename:
            return

        path = self.get_sound_path(filename)

        try:
            pygame.mixer.music.load(path)

            # Use the normal music volume, or 0 if muted.
            if self.muted:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.music_volume)

            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play(0)

            self.current_music = filename

        except pygame.error:
            pass
        except FileNotFoundError:
            pass

    def stop_music(self):
        """
        Stop the current background music.
        """
        if not self.sound_enabled:
            return

        pygame.mixer.music.stop()
        self.current_music = None