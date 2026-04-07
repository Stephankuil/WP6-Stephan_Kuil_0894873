import pygame
from Home_screen import HomeScreen
from Game_window import GameWindow
from LEVEL import Levelmap
from Pacman import Pacman
from Game import Game1


def main():
    pygame.init()

    breedte = 850
    hoogte = 600
    window = pygame.display.set_mode((breedte, hoogte))

    home_screen = HomeScreen(window, breedte, hoogte)
    keuze = home_screen.run()

    if keuze == "start":
        game_window = GameWindow(breedte, hoogte)
        levelmap = Levelmap()

        pacman = Pacman(
            levens=3,
            Xcoordinaat=1,
            Ycoordinaat=1,
            score=0,
            kleur=(255, 255, 0),
            naam="Pacman"
        )

        game = Game1.Game(levelmap, pacman)
        game_window.run(game)


if __name__ == "__main__":
    main()