class Spook:
    def __init__(self, naam, kleur, x_coordinaat, y_coordinaat, opeetbaar):
        if not isinstance(naam, str):
            raise ValueError("naam moet een string zijn")
        if not isinstance(kleur, str):
            raise ValueError("kleur moet een string zijn")

        self.naam = naam
        self.kleur = kleur
        self.x_coordinaat = x_coordinaat
        self.y_coordinaat = y_coordinaat
        self.opeetbaar = opeetbaar



    def hitpacman(self, pacman):
        if self.opeetbaar:
            pacman.score += 10
        else:
            pacman.levens -= 1



