import pygame
from Spookjes import Spook
class Game:
    def __init__(self, levelmap, pacman):
        self.levelmap = levelmap
        self.pacman = pacman
        self.spookjes = [
            Spook(10, 5, 200, (255, 0, 0), "Blinky", False),
            Spook(12, 10, 200, (255, 105, 180), "Pinky", False)
        ]

    def handle_input(self, event):
        oude_x = self.pacman.Xcoordinaat
        oude_y = self.pacman.Ycoordinaat

        if event.key == pygame.K_UP:
            self.pacman.move("up")
        elif event.key == pygame.K_DOWN:
            self.pacman.move("down")
        elif event.key == pygame.K_LEFT:
            self.pacman.move("left")
        elif event.key == pygame.K_RIGHT:
            self.pacman.move("right")

        if self.levelmap.is_wall(self.pacman.Xcoordinaat, self.pacman.Ycoordinaat):
            self.pacman.Xcoordinaat = oude_x
            self.pacman.Ycoordinaat = oude_y