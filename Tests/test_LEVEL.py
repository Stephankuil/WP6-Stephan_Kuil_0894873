import pytest
from Game.LEVEL import Levelmap


def test_level():
    level = Levelmap()
    assert level.LEVEL_MAP1 is not None
    assert level.LEVEL_MAP2 is not None




############################################

#unhappy path

def test_level_unhappy():
    level = Levelmap()
    assert level.get_tile_level1(100, 100) is None
    assert level.get_tile_level2(100, 100) is None
