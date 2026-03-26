from Game.Kaasjes import Kaas

class Levelmap:
    def __init__(self):
        self.LEVEL_MAP1 = [
            "############################",
            "#            ##            #",
            "# #### ##### ## ##### #### #",
            "# #### ##### ## ##### #### #",
            "# #### ##### ## ##### #### #",
            "#                          #",
            "# #### ## ######## ## #### #",
            "# #### ## ######## ## #### #",
            "#      ##    ##    ##      #",
            "###### ##### ## ##### ######",
            "###### ##### ## ##### ######",
            "       ##          ##       ",
            "###### ## ###  ### ## ######",
            "###### ## #      # ## ######",
            "#                          #",
            "# #### ########## #### ### #",
            "# #### ########## #### ### #",
            "#                          #",
            "############################",
        ]

        self.LEVEL_MAP2 = [
            "##############################",
            "              ##             #",
            "#   ##    ##  ##    ##  ##   #",
            "#   ##    ##  ##    ##  ##   #",
            "#             ##             #",
            "#   ########      #########  #",
            "#                            #",
            "#    #   #     #    #####    #",
            "#    #   #     #        #    #",
            "#    #####     #        #    #",
            "#              #    #####    #",
            "#                            #",
            "#    ####  #####   ########  #",
            "#          #####    #####    #",
            "#      #                     #",
            "#      #              ##     #",
            "#    ########     #########  #",
            "#                             ",
            "##############################",
        ]

        self.current_map = self.LEVEL_MAP1
        self.kaasjes = Kaas(self._find_kaas_posities())

    def is_wall(self, x, y):
        return self.get_tile(x, y) == "#"

    def get_tile(self, x, y):
        if 0 <= y < len(self.current_map) and 0 <= x < len(self.current_map[y]):
            return self.current_map[y][x]
        return None

    def get_tile_level1(self, x, y):
        if 0 <= y < len(self.LEVEL_MAP1) and 0 <= x < len(self.LEVEL_MAP1[y]):
            return self.LEVEL_MAP1[y][x]
        return None

    def get_tile_level2(self, x, y):
        if 0 <= y < len(self.LEVEL_MAP2) and 0 <= x < len(self.LEVEL_MAP2[y]):
            return self.LEVEL_MAP2[y][x]
        return None

    def _find_kaas_posities(self):
        posities = []

        for y, row in enumerate(self.current_map):
            for x, ch in enumerate(row):
                if ch == " ":
                    posities.append((x, y))

        return posities