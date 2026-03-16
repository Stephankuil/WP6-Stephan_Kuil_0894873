import pytest

from Game.Spookjes import Spookjes

#Happy Path Test######################################

def test_spookjes_initialization():
    spookjes = Spookjes(4, "Blinky", "rood", 5, 5, True)
    assert spookjes.aantal_spookjes == 4
    assert spookjes.naam == "Blinky"
    assert spookjes.kleur == "rood"
    assert spookjes.x_coordinaat == 5
    assert spookjes.y_coordinaat == 5
    assert spookjes.opeetbaar == True


#Unhappy Path Test######################################

def test_spookjes_initialization_unhappy():
    with pytest.raises(ValueError):
        spookjes = Spookjes("-1", "Blinky", "rood", 5, 5, True)