"""Test interp.py"""


import pytest


SELF_EVALUATING = [0, 10, False, True]


@pytest.fixture
def test_env():
    """Test environment fixture."""
    from interp import empty_env, env_extend
    return env_extend({'a': 1},
                      env_extend({'b': 2},
                                 env_extend({'a': 0}, empty_env)))


@pytest.fixture
def primitive_min():
    """Primitive function like Python's 'min'.

    But only the 2 arity version."""
    from interp import primitive_function
    return primitive_function(min, 2)


@pytest.fixture
def identity():
    """The identity function represented as a compound function."""
    from interp import compound_function, empty_env
    return compound_function(['x'], 'x', empty_env)


def test_env_lookup():
    """Test looking up variable in one-frame env."""
    from interp import empty_env, env_lookup, env_extend
    assert env_lookup(env_extend({'a': 0}, empty_env), 'a') == 0


def test_env_lookup_lexical(test_env):
    """Test looking up variable lexically."""
    from interp import env_lookup
    assert env_lookup(test_env, 'a') == 1


def test_env_lookup_deep(test_env):
    """Test looking up variable not local."""
    from interp import env_lookup
    assert env_lookup(test_env, 'b') == 2


def test_env_lookup_failure(test_env):
    """Test env_lookup throws KeyError on var not found."""
    from interp import env_lookup
    with pytest.raises(KeyError):
        env_lookup(test_env, '')


@pytest.mark.parametrize('x', SELF_EVALUATING)
def test_self_evaluating(x):
    """Test evaluate simply returns self-evaluating value."""
    from interp import evaluate, empty_env
    assert evaluate(x, empty_env) == x


def test_evaluate_variable(test_env):
    """Test evaluate looks up variable in environment."""
    from interp import evaluate
    assert evaluate('a', test_env) == 1


def test_closure_application(identity):
    from interp import apply_function
    """Test application of compound function."""
    assert apply_function(identity, [0]) == 0


def test_evaluate_compound(identity):
    """Test evaluate_compound applies function."""
    from interp import evaluate_compound, empty_env
    assert evaluate_compound(identity, [0], empty_env) == 0


def test_evaluate_compound_evaluate_identity():
    """Test evaluate_compound evaluates a function."""
    from interp import evaluate_compound, empty_env
    op = evaluate_compound('lambda', [['x'], 'x'], empty_env)
    assert evaluate_compound(op, [0], empty_env) == 0


def test_evaluate_evaluates_compounds():
    """Test evaluate correctly evaluates compound expressions."""
    from interp import evaluate, empty_env
    assert evaluate([['lambda', ['x'], 'x'], 0], empty_env) == 0


def test_primitive_function(primitive_min):
    """Test application of primitive function.

    Primitive functions are functions which are coded in Python. This
    is analogous to functions written in C in Python."""
    from interp import apply_function
    assert apply_function(primitive_min, [1, 2]) == 1


def test_primitive_function_not_enough_args(primitive_min):
    """Test primitive_function raises TypeError for less than enough args."""
    from interp import apply_function
    with pytest.raises(TypeError):
        apply_function(primitive_min, [1])


def test_primitive_function_too_many_args(primitive_min):
    """Test primitive_function raises TypeError for more than enough args."""
    from interp import apply_function
    with pytest.raises(TypeError):
        apply_function(primitive_min, [1, 2, 3])


def test_compound_begin():
    """Test begin returns argument."""
    from interp import evaluate_compound, empty_env
    assert evaluate_compound('begin', [1], empty_env) == 1


def test_compound_begin_returns_last_arg():
    """Test begin returns argument."""
    from interp import evaluate_compound, empty_env
    assert evaluate_compound('begin', [1, 2], empty_env) == 2


def test_evaluate_lambda():
    from interp import evaluate_lambda, evaluate, empty_env
    op = evaluate_lambda([['x'], 'x'], empty_env)
    assert evaluate([op, 0], empty_env) == 0
