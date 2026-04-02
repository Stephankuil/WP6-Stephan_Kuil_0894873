class Kaas:
    def __init__(self, kaas_posities, kleur=(255, 255, 0)):  # geel
        self.kaas_posities = set(kaas_posities)
        self.kleur = kleur




    def eet_kaas(self, x, y):
        if (x, y) in self.kaas_posities:
            self.kaas_posities.remove((x, y))
            return True
        return False

    def aantal_over(self):
        return len(self.kaas_posities)