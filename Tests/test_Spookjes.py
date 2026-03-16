import pytest

from Game.Spookjes import Spookjes

#Happy Path Test######################################

def test_spookjes_initialization():
    spookje = Spookjes("Blinky", "rood", 5, 5, True)
    assert spookje.naam == "Blinky"
    assert spookje.kleur == "rood"
    assert spookje.x_coordinaat == 5
    assert spookje.y_coordinaat == 5
    assert spookje.opeetbaar == True


def test_hitpacman_opeetbaar():
    spookje = Spookjes("Blinky", "rood", 5, 5, True)
    class MockPacman:
        def __init__(self):
            self.score = 0
            self.levens = 3

    pacman = MockPacman()
    spookje.hitpacman(pacman)
    assert pacman.score == 10
    assert pacman.levens == 3


#unhappy path test######################################

def test_hitpacman_onopeetbaar_unhappy():
    spookje = Spookjes("Blinky", "rood", 5, 5, False)
    class MockPacman:
        def __init__(self):
            self.score = 0
            self.levens = 3

    pacman = MockPacman()
    spookje.hitpacman(pacman)
    assert pacman.score == 0
    assert pacman.levens == 3

def test_spookjes_initialization_unhappy():
    with pytest.raises(ValueError):
        spookje = Spookjes(123, "rood", 5, 5, True)

    with pytest.raises(ValueError):
        spookje = Spookjes("Blinky", 456, 5, 5, True)
