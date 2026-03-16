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


def test_pacman_move():
    pacman = Pacman(3, 0, 0, 0, "geel", "Pacman")
    pacman.move("up")
    assert pacman.Ycoordinaat == 1
    pacman.move("down")
    assert pacman.Ycoordinaat == 0
    pacman.move("left")
    assert pacman.Xcoordinaat == -1
    pacman.move("right")
    assert pacman.Xcoordinaat == 0

def test_pacman_move_invalid_direction():
    pacman = Pacman(3, 0, 0, 0, "geel", "Pacman")
    pacman.move("invalid_direction")
    assert pacman.Xcoordinaat == 0
    assert pacman.Ycoordinaat == 0
#unhappy path test######################################
def test_pacman_initialization_unhappy():
    with pytest.raises(ValueError):
        pacman = Pacman("-1", 0, 0, 0, "geel", "Pacman")