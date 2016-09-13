"""Test interp.py"""

import pytest


BALANCED_TABLE = [
    ('', True),
    ('()', True),
    ('(() (() ()))', True),
    ('(', False),
    ('(()', False),
    ('(() (() ())', False),
    ('hello', True),
    ('(test test)', True),
    ('(test () (hello() (world)))', True),
    ('(test', False),
    ('((test)', False),
    ('(f (f) (f f f () ())', False)
]

UNBALANCED_TABLE = [')', '(((()))))', '())))))) ((', '(() () ()))']


@pytest.mark.parametrize('s, expected', BALANCED_TABLE)
def test_balanced(s, expected):
    """Test balanced."""
    from interp import balanced
    assert balanced(s) == expected


@pytest.mark.parametrize('s', UNBALANCED_TABLE)
def test_unbalanced(s):
    """Test unbalanced inputs."""
    from interp import balanced
    with pytest.raises(ValueError):
        balanced(s)
