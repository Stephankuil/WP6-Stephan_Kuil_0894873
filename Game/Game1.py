import pygame
from Game.Spookjes import Spook
from Game.Pacman import Pacman
from Game.Engine import Engine
import time
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
        """
        Check if Pacman collides with a ghost.

        There are 2 possible outcomes:
        1. If the ghost is edible, Pacman eats the ghost
        2. If the ghost is not edible, the ghost damages Pacman

        A small cooldown is used so that collisions are not triggered
        many times in a row within a very short time.
        """

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # Only allow a new collision if at least 1000 ms passed
        # since the last collision
        if current_time - self.last_hit_time > 1000:

            # Check collision against every ghost in the game
            for spook in self.spookjes:

                # Check if Pacman and this ghost are on the same tile
                if (
                        spook.Xcoordinaat == self.pacman.Xcoordinaat and
                        spook.Ycoordinaat == self.pacman.Ycoordinaat
                ):

                    # -------------------------------------------------
                    # CASE 1: Ghost is edible
                    # -------------------------------------------------
                    if spook.opeetbaar:
                        print(f"Pacman eats ghost {spook.naam}!")

                        # Give Pacman points for eating the ghost
                        self.pacman.score += 200

                        # Reset ghost to its starting position
                        spook.reset_positie()

                        # Make the ghost normal again after being eaten
                        spook.maak_normaal()

                        print(f"Pacman score: {self.pacman.score}, levens: {self.pacman.levens}")

                    # -------------------------------------------------
                    # CASE 2: Ghost is dangerous
                    # -------------------------------------------------
                    else:
                        print("Pacman raakt spookje!")
                        spook.raak_pacman(self.pacman)
                        print(f"Pacman score: {self.pacman.score}, levens: {self.pacman.levens}")

                    # Update collision cooldown timer
                    self.last_hit_time = current_time


    def Pacman_eet_kaas(self):
        Pacman.kaasje_opeten(self.pacman, self.levelmap.kaasjes)

    def activeer_power_mode(self):
        """
        Activate power mode: all ghosts become edible.
        """
        self.power_mode = True
        self.power_mode_eind_tijd = time.time() + 8  # 8 seconds

        for spook in self.spookjes:
            spook.maak_opeetbaar()

        print("Power mode ACTIVATED!")

    def update_power_mode(self):
        """
        Disable power mode after timer ends.
        """
        if self.power_mode and time.time() > self.power_mode_eind_tijd:
            self.power_mode = False

            for spook in self.spookjes:
                spook.maak_normaal()

            print("Power mode ENDED!")



    def check_game_over(self):
        if self.pacman.levens == 0:
            self.pacman.add_score()
            self.pacman.levens = -1
            print("Game over! Score opgeslagen.")
            return True
        return False

