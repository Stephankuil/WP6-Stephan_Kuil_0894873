class Pacman:
    def __init__(self, levens, Xcoordinaat, Ycoordinaat, score, kleur, naam):
        if not isinstance(levens, int):
            raise ValueError("levens moet een integer zijn")

        if levens < 0:
            raise ValueError("levens mag niet negatief zijn")
        self.levens = levens
        self.Xcoordinaat = Xcoordinaat
        self.Ycoordinaat = Ycoordinaat
        self.score = score
        self.kleur = kleur
        self.naam = naam

    def move(self, direction):
        if direction == "up":
            self.Ycoordinaat += 1
        elif direction == "down":
            self.Ycoordinaat -= 1
        elif direction == "left":
            self.Xcoordinaat -= 1
        elif direction == "right":
            self.Xcoordinaat += 1




