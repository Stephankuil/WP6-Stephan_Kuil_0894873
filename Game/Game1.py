import pygame

class Game:
    def __init__(self, levelmap, pacman):
        self.levelmap = levelmap
        self.pacman = pacman

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