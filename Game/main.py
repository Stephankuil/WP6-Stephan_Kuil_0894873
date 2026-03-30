import pygame
from Game_window import GameWindow
from LEVEL import Levelmap
from Kaasjes import Kaas
from sys import exit
from Spookjes import Spook
from Pacman import Pacman
from Game import Game1

def main():
    pygame.init()
    game_window = GameWindow(850, 600)
    levelmap = Levelmap()
    kaas = draw_kaas = Kaas(levelmap._find_kaas_posities())
    spook = Spook("bob", "geel", 10, 10, 0)
    pacman = Pacman(
        levens=3,Xcoordinaat=1,Ycoordinaat=1,score=0,kleur=(255, 0, 255),naam="Pacman"
    )

    game = Game1.Game(levelmap, pacman)
    game_window.run(game)

if __name__ == "__main__":
    main()

#hallo
