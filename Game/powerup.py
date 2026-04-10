import random


class PowerUp:
    def __init__(self, kleur=(0, 255, 255)):
        """
        This class manages one power-up on the map.

        Responsibilities:
        - store the current power-up position
        - spawn the power-up at a random valid location
        - detect if Pacman picked it up
        """

        self.kleur = kleur

        # None means: currently no power-up is visible on the map
        self.positie = None

    def spawn_random(self, vrije_posities):
        """
        Spawn the power-up at a random valid position.

        Parameters:
        vrije_posities: a list or set of walkable positions like:
                        [(1, 1), (2, 1), (3, 4), ...]

        The power-up only spawns if there is currently no active one.
        """
        if self.positie is None and vrije_posities:
            self.positie = random.choice(list(vrije_posities))

    def verwijder(self):
        """
        Remove the current power-up from the map.
        """
        self.positie = None

    def is_opgepakt(self, x, y):
        """
        Check if Pacman is standing on the power-up.

        Returns True if Pacman picked it up, otherwise False.
        """
        if self.positie == (x, y):
            self.verwijder()
            return True
        return False