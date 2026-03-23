import pytest
from Game.LEVEL import Levelmap


def test_level():
    level = Levelmap()
    assert level.LEVEL_MAP1 is not None
    assert level.LEVEL_MAP2 is not None
