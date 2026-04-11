import pygame
import time
from Game.Spookjes import Spook
from Game.Pacman import Pacman


class Game:
    def __init__(self, levelmap, pacman, mqtt_handler):
        self.levelmap = levelmap
        self.pacman = pacman
        self.mqtt_handler = mqtt_handler

        self.spookjes = [
            Spook(10, 5, 200, (255, 0, 0), "Blinky", False),
            Spook(12, 10, 200, (255, 105, 180), "Pinky", False),
            Spook(8, 8, 200, (255, 105, 180), "Pinky", False),
            Spook(6, 6, 200, (255, 105, 180), "Pinky", False)
        ]

        self.last_hit_time = 0
        self.game_over = False

        # Belangrijk: deze moeten bestaan, anders krijg je weer attribute errors
        self.power_mode = False
        self.power_mode_eind_tijd = 0

    # ---------------------------------------------------------
    # INPUT
    # ---------------------------------------------------------

    def handle_input(self, event):
        """
        In multiplayer sturen we alleen input naar de host.
        De host beslist daarna hoe spelers echt bewegen.
        """
        if event.key == pygame.K_UP:
            self.mqtt_handler.send_input("up")
        elif event.key == pygame.K_DOWN:
            self.mqtt_handler.send_input("down")
        elif event.key == pygame.K_LEFT:
            self.mqtt_handler.send_input("left")
        elif event.key == pygame.K_RIGHT:
            self.mqtt_handler.send_input("right")

    # ---------------------------------------------------------
    # MULTIPLAYER HOST LOGIC
    # ---------------------------------------------------------

    def process_network_inputs(self):
        """
        Alleen de host verwerkt ontvangen inputs.
        """
        for input_data in self.mqtt_handler.pop_received_inputs():
            player_id = input_data.get("player_id")
            direction = input_data.get("direction")

            if not player_id or not direction:
                continue

            self.mqtt_handler.set_player_direction(player_id, direction)

    def update_multiplayer_players(self):
        """
        Alleen de host beweegt alle spelers.
        Eerst berekenen we nieuwe positie, daarna checken we muurcollision.
        """
        for player_id, player in self.mqtt_handler.players_state.items():
            direction = player["direction"]

            oude_x = player["x"]
            oude_y = player["y"]

            nieuwe_x = oude_x
            nieuwe_y = oude_y

            if direction == "up":
                nieuwe_y -= 1
            elif direction == "down":
                nieuwe_y += 1
            elif direction == "left":
                nieuwe_x -= 1
            elif direction == "right":
                nieuwe_x += 1

            # Alleen bewegen als er geen muur staat
            if not self.levelmap.is_wall(nieuwe_x, nieuwe_y):
                player["x"] = nieuwe_x
                player["y"] = nieuwe_y

    def sync_local_pacman_from_mqtt(self):
        """
        Zet de lokale pacman gelijk aan zijn MQTT state.
        Dit is handig zodat bestaande singleplayer logica
        voorlopig nog blijft werken voor de lokale speler.
        """
        local_player = self.mqtt_handler.get_local_player()

        if local_player is None:
            return

        self.pacman.Xcoordinaat = local_player["x"]
        self.pacman.Ycoordinaat = local_player["y"]
        self.pacman.score = local_player["score"]
        self.pacman.levens = local_player["lives"]

    def sync_mqtt_from_local_pacman(self):
        """
        Schrijf wijzigingen uit oude game logica terug naar MQTT state.
        Bijvoorbeeld score/levens van de host-speler.
        """
        local_player = self.mqtt_handler.get_local_player()

        if local_player is None:
            return

        local_player["x"] = self.pacman.Xcoordinaat
        local_player["y"] = self.pacman.Ycoordinaat
        local_player["score"] = self.pacman.score
        local_player["lives"] = self.pacman.levens

    def host_tick(self):
        """
        Deze methode roept de host elke frame aan.
        """
        self.process_network_inputs()
        self.update_multiplayer_players()
        self.sync_local_pacman_from_mqtt()

        # Oude singleplayer logica tijdelijk alleen voor host-speler
        self.Pacman_eet_kaas()
        self.Pacman_Raakt_Spook()
        self.update_power_mode()
        self.check_game_over()

        self.sync_mqtt_from_local_pacman()
        self.mqtt_handler.send_game_state()

    # ---------------------------------------------------------
    # OUDE GAME LOGIC
    # ---------------------------------------------------------

    def Pacman_Raakt_Spook(self):
        """
        Check if the local Pacman collides with a ghost.
        Tijdelijk werkt dit alleen voor de lokale speler/host.
        """
        current_time = pygame.time.get_ticks()

        if current_time - self.last_hit_time > 1000:
            for spook in self.spookjes:
                if (
                    spook.Xcoordinaat == self.pacman.Xcoordinaat and
                    spook.Ycoordinaat == self.pacman.Ycoordinaat
                ):
                    if spook.opeetbaar:
                        print(f"Pacman eats ghost {spook.naam}!")
                        self.pacman.score += 200
                        spook.reset_positie()
                        spook.maak_normaal()
                        print(f"Pacman score: {self.pacman.score}, levens: {self.pacman.levens}")
                    else:
                        print("Pacman raakt spookje!")
                        spook.raak_pacman(self.pacman)
                        print(f"Pacman score: {self.pacman.score}, levens: {self.pacman.levens}")

                    self.last_hit_time = current_time

    def Pacman_eet_kaas(self):
        Pacman.kaasje_opeten(self.pacman, self.levelmap.kaasjes)

    def activeer_power_mode(self):
        """
        Activate power mode: all ghosts become edible.
        """
        self.power_mode = True
        self.power_mode_eind_tijd = time.time() + 8

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