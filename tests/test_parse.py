"""Test parse.py."""

import pytest


LEX_RESULTS = [
    ('', []),
    ('()', ['(', ')']),
    ('x', ['x']),
    ('x y', ['x', 'y']),
    ('(x y)', ['(', 'x', 'y', ')']),
    ('(x (y))', ['(', 'x', '(', 'y', ')', ')']),
    ('0', [0]),
    ('(0)', ['(', 0, ')']),
    ('((0) (f))', ['(', '(', 0, ')', '(', 'f', ')', ')']),
    ('((15) (f))', ['(', '(', 15, ')', '(', 'f', ')', ')'])
]


PARSE_RESULTS = [
    (['(', ')'], []),
    (['x'], 'x'),
    (['x', 'y'], 'x'),
    (['(', 'x', 'y', ')'], ['x', 'y']),
    (['(', 'x', '(', 'y', ')', ')'], ['x', ['y']])
]


READ_RESULTS = [
    ('()', []),
    ('x', 'x'),
    ('x y', 'x'),
    ('(x y)', ['x', 'y']),
    ('(x (y))', ['x', ['y']]),
    ('0', 0),
    ('(0)', [0]),
    ('((0) (f))', [[0], ['f']]),
    ('((15) (f))', [[15], ['f']])
]


@pytest.mark.parametrize('string, tokens', LEX_RESULTS)
def test_lex(string, tokens):
    """Test lex."""
    from src.parse import lex
    assert lex(string) == tokens


@pytest.mark.parametrize('tokens, tree', PARSE_RESULTS)
def test_parse(tokens, tree):
    """Test parse."""
    from src.parse import parse
    assert parse(tokens) == tree


@pytest.mark.parametrize('string, tree', READ_RESULTS)
def test_read_string(string, tree):
    """Test read_string."""
    from src.parse import read_string
    assert read_string(string) == tree
