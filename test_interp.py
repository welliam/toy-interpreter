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

def test_cons_str_simple():
    from interp import cons
    assert str(cons(1, 2)) == '(1 . 2)'


def test_cons_str_embedded():
    from interp import cons
    assert str(cons(cons(1, 2), cons(1, 2))) == '((1 . 2) . (1 . 2))'


def test_cons_str_linked():
    from interp import cons
    assert str(cons(1, cons(2, 3))) == '(1 . (2 . 3))'


def test_list_str_empty():
    from interp import null
    assert str(null) == '()'


def test_list_str_simple():
    from interp import cons, null
    assert str(cons(1, null)) == '(1)'


def test_list_str_long():
    from interp import cons, null
    assert str(cons(1, (cons(2, cons(3, null))))) == '(1 2 3)'


def test_list_str_embedded():
    from interp import cons, null
    lst = cons(cons(1, cons(2, null)), cons(3, cons(4, null)))
    assert str(lst) == '((1 2) 3 4)'
