import pygame
from Game.Game_window import GameWindow
from Game.LEVEL import Levelmap
from Game.Kaasjes import Kaas
from sys import exit
from Spookjes import Spook


def main():
    pygame.init()
    game_window = GameWindow(800, 600)
    levelmap = Levelmap()
    spook = Spook("bob", "geel", 10, 10, 0)

    game_window.run(levelmap)

if __name__ == "__main__":
    main()