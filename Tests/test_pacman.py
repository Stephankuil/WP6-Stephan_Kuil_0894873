import pytest

from Game.Pacman import Pacman


#Happy Path Test######################################

def test_pacman_initialization():
    pacman = Pacman(3, 0, 0, 0, "geel", "Pacman")
    assert pacman.levens == 3
    assert pacman.Xcoordinaat == 0
    assert pacman.Ycoordinaat == 0
    assert pacman.score == 0
    assert pacman.kleur == "geel"
    assert pacman.naam == "Pacman"

def test_pacman_initialization_unhappy():
    with pytest.raises(ValueError):
        pacman = Pacman("-1", 0, 0, 0, "geel", "Pacman")