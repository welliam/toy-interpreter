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
    ('((0) (f))', ['(', '(', 0, ')', '(', 'f', ')', ')'])
    ('((15.5) (f))', ['(', '(', 15, ')', '(', 'f', ')', ')'])
]


PARSE_RESULTS = [
    (['(', ')'], []),
    (['x'], 'x'),
    (['x', 'y'], 'x'),
    (['(', 'x', 'y', ')'], ['x', 'y']),
    (['(', 'x', '(', 'y', ')', ')'], ['x', ['y']])
]


@pytest.mark.parametrize('string, tokens', LEX_RESULTS)
def test_lex(string, tokens):
    """Test lex."""
    from parse import lex
    assert lex(string) == tokens


@pytest.mark.parametrize('tokens, tree', PARSE_RESULTS)
def test_parse(tokens, tree):
    """Test parse."""
    from parse import parse
    assert parse(tokens) == tree
