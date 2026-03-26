import pytest
import pygame
from sys import exit


from Game.Game_window import GameWindow

#Happy Path Test######################################


def test_game_window_initialization():
    pygame.init()
    game_window = GameWindow(800, 600)
    assert game_window.breedte == 800
    assert game_window.hoogte == 600
    assert isinstance(game_window.window, pygame.Surface)
    game_window.exit_game()

#unhappy path test######################################

