import pytest
from Game.Game1 import Game
from Game.LEVEL import Levelmap
from Game.Pacman import Pacman
from Game.Spookjes import Spook
def test_Game1():


    levelmap = Levelmap()
    pacman = Pacman(
        levens=3,
        Xcoordinaat=1,
        Ycoordinaat=1,
        score=0,
        kleur=(255, 255, 0),
        naam="Pacman"
    )

    game = Game(levelmap, pacman)

    assert game.levelmap == levelmap
    assert game.pacman == pacman


#############################################

#unhappy path

    with pytest.raises(ValueError):
        Pacman(
            levens=-1,
            Xcoordinaat=1,
            Ycoordinaat=1,
            score=0,
            kleur=(255, 255, 0),
            naam="Pacman"
        )

    with pytest.raises(ValueError):
        Pacman(
            levens="three",
            Xcoordinaat=1,
            Ycoordinaat=1,
            score=0,
            kleur=(255, 255, 0),
            naam="Pacman"
        )