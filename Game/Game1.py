import pygame
from Spookjes import Spook
from Pacman import Pacman
from Engine import Engine
class Game:
    def __init__(self, levelmap, pacman):
        self.levelmap = levelmap
        self.pacman = pacman
        self.spookjes = [
            Spook(10, 5, 200, (255, 0, 0), "Blinky", False),
            Spook(12, 10, 200, (255, 105, 180), "Pinky", False),
            Spook(8, 8, 200, (255, 105, 180), "Pinky", False),
            Spook(6, 6, 200, (255, 105, 180), "Pinky", False)
        ]
        self.last_hit_time = 0
        self.game_over = False


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

    def Pacman_Raakt_Spook(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > 1000:
            for spook in self.spookjes:
                if spook.Xcoordinaat == self.pacman.Xcoordinaat and spook.Ycoordinaat == self.pacman.Ycoordinaat:
                    print("Pacman raakt spookje!")
                    spook.raak_pacman(self.pacman)
                    print(f"Pacman score: {self.pacman.score}, levens: {self.pacman.levens}")
                    self.last_hit_time = current_time


    def Pacman_eet_kaas(self):
        Pacman.kaasje_opeten(self.pacman, self.levelmap.kaasjes)

    def check_game_over(self):
        if self.pacman.levens == 0:
            self.pacman.add_score()
            self.pacman.levens = -1
            print("Game over! Score opgeslagen.")
            return True
        return False

