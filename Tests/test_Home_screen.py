import pytest
import pygame

from Game.Home_screen import HomeScreen

def test_HomeScreen():
    pygame.init()
    # Mock window and dimensions
    class MockWindow:
        def fill(self, color):
            pass

        def blit(self, source, dest):
            pass

    mock_window = MockWindow()
    breedte = 850
    hoogte = 600

    home_screen = HomeScreen(mock_window, breedte, hoogte)

    assert home_screen.window == mock_window
    assert home_screen.breedte == breedte
    assert home_screen.hoogte == hoogte


    #####################################33
    #unhappy path

    def test_HomeScreen_invalid_window():
        pygame.init()

        with pytest.raises(TypeError):
            HomeScreen("not a window", 850, 600)