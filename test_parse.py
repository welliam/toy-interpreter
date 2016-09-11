"""Test parse.py."""

import pytest


LEX_RESULTS = [
    ('', []),
    ('()', ['(', ')']),
    ('x', ['x']),
    ('x y', ['x', 'y']),
    ('(x y)', ['(', 'x', 'y', ')']),
    ('(x (y))', ['(', 'x', '(', 'y', ')', ')'])
]


@pytest.mark.parametrize('string, tokens', LEX_RESULTS)
def test_lex(string, tokens):
    """Test lex."""
    from parse import lex
    assert lex(string) == tokens
