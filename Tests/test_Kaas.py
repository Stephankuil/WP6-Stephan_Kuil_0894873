import pytest
from Game.level import Levelmap
from Game.Kaasjes import Kaas

#Happy Path Test######################################

def test_kaas_eet():
    kaas = Kaas([(1, 1), (2, 2)])

    assert kaas.eet_kaas(1, 1) is True
    assert kaas.eet_kaas(1, 1) is False
    assert kaas.aantal_over() == 1



#unhappy path test######################################

def test_kaas_eet_unhappy():
    kaas = Kaas([(1, 1), (2, 2)])

    assert kaas.eet_kaas(3, 3) is False
    assert kaas.aantal_over() == 2