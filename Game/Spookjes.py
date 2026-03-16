class Spookjes:
    def __init__(self, aantal_spookjes, naam, kleur, x_coordinaat, y_coordinaat, opeetbaar):
            if not isinstance(aantal_spookjes, int):
                raise ValueError("aantal_spookjes moet een integer zijn")
            if aantal_spookjes < 0:
                raise ValueError("aantal_spookjes mag niet negatief zijn")
            self.aantal_spookjes = aantal_spookjes
            self.naam = naam
            self.kleur = kleur
            self.x_coordinaat = x_coordinaat
            self.y_coordinaat = y_coordinaat
            self.opeetbaar = opeetbaar



