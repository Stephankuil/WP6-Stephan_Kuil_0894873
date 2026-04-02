import pygame
import random

class Spook:
    def __init__(self, Xcoordinaat, Ycoordinaat, score, kleur, naam, opeetbaar):

        self.Xcoordinaat = Xcoordinaat
        self.Ycoordinaat = Ycoordinaat
        self.score = score
        self.kleur = kleur
        self.naam = naam
        self.opeetbaar = opeetbaar
        self.last_move_time = 0
        self.move_delay = 300  # milliseconden

    def move(self, direction):
        if direction == "up":
            self.Ycoordinaat -= 1
        elif direction == "down":
            self.Ycoordinaat += 1
        elif direction == "left":
            self.Xcoordinaat -= 1
        elif direction == "right":
            self.Xcoordinaat += 1

    def move_met_muurcheck(self, direction, levelmap):
        oude_x = self.Xcoordinaat
        oude_y = self.Ycoordinaat

        self.move(direction)

        if levelmap.is_wall(self.Xcoordinaat, self.Ycoordinaat):
            self.Xcoordinaat = oude_x
            self.Ycoordinaat = oude_y

    def random_move(self, levelmap):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_move_time > self.move_delay:
            direction = random.choice(["up", "down", "left", "right"])
            self.move_met_muurcheck(direction, levelmap)
            self.last_move_time = current_time


    def raak_pacman(self, pacman):
        if self.opeetbaar:
            pacman.score += self.score
        else:
            pacman.levens -= 1

    def draw(self, window, tile_size):
        pygame.draw.circle(
            window,
            self.kleur,
            (
                self.Xcoordinaat * tile_size + tile_size // 2,
                self.Ycoordinaat * tile_size + tile_size // 2
            ),
            tile_size // 2 - 2
        )