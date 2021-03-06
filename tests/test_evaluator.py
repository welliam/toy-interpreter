"""Test evaluator.py"""


import pytest


SELF_EVALUATING = [0, 10, False, True]


PROGRAMS = [
    (0, ['begin',
         ['define', 'id', ['lambda', ['x'], 'x']],
         ['define', 'x', 0],
         ['id', 'x']]),
    (1, ['begin',
         ['define', 'const',
          ['lambda', ['x'],
           ['lambda', ['y'], 'x']]],
         [['const', 1], 2]]),
    (0, ['begin',
         ['define', 'x',
          ['if', ['if', True, False, True], 1, 0]],
         [['lambda', ['x'], 'x'], 'x']]),
    (0, ['begin',
         ['if', True,
          ['define', 'x', 0],
          ['define', 'x', 1]],
         'x']),
    (1, ['begin',
         ['if', False,
          ['define', 'x', 0],
          ['define', 'x', 1]],
         'x']),
    (0, [['lambda', ['x', 'y'], 'x'], 0, 1]),
    (1, [['lambda', ['x', 'y'], 'y'], 0, 1]),
    (0, ['begin',
         ['define', 'x', 0],
         ['define', 'f',
          ['lambda', [],
           ['define', 'x', 1]]],
         ['f'],
         'x']),
    (1, ['begin',
         ['define', 'x', 0],
         ['define', 'f',
          ['lambda', [],
           ['set!', 'x', 1]]],
         ['f'],
         'x'])
]


@pytest.fixture
def fresh_env():
    """Return an empty environment."""
    from src.evaluator import make_env
    return make_env()


@pytest.fixture
def test_env(fresh_env):
    """Test environment fixture."""
    from src.evaluator import env_extend
    return env_extend({'a': 1},
                      env_extend({'b': 2},
                                 env_extend({'a': 0}, fresh_env)))


@pytest.fixture
def primitive_min():
    """Primitive function like Python's 'min'.

    But only the 2 arity version."""
    from src.evaluator import primitive_function
    return primitive_function(min, 2)


@pytest.fixture
def identity(fresh_env):
    """The identity function represented as a compound function."""
    from src.evaluator import compound_function
    return compound_function(['x'], 'x', fresh_env)


@pytest.mark.parametrize('output, program', PROGRAMS)
def test_program(output, program, fresh_env):
    """Test program produces given output."""
    from src.evaluator import evaluate
    assert evaluate(program, fresh_env) == output


def test_env_lookup(fresh_env):
    """Test looking up variable in one-frame env."""
    from src.evaluator import env_lookup, env_extend
    assert env_lookup(env_extend({'a': 0}, fresh_env), 'a') == 0


def test_env_lookup_lexical(test_env):
    """Test looking up variable lexically."""
    from src.evaluator import env_lookup
    assert env_lookup(test_env, 'a') == 1


def test_env_lookup_deep(test_env):
    """Test looking up variable not local."""
    from src.evaluator import env_lookup
    assert env_lookup(test_env, 'b') == 2


def test_env_lookup_failure(test_env):
    """Test env_lookup throws KeyError on var not found."""
    from src.evaluator import env_lookup
    with pytest.raises(KeyError):
        env_lookup(test_env, '')


@pytest.mark.parametrize('x', SELF_EVALUATING)
def test_self_evaluating(x, fresh_env):
    """Test evaluate simply returns self-evaluating value."""
    from src.evaluator import evaluate
    assert evaluate(x, fresh_env) == x


def test_evaluate_variable(test_env):
    """Test evaluate looks up variable in environment."""
    from src.evaluator import evaluate
    assert evaluate('a', test_env) == 1


def test_closure_application(identity):
    from src.evaluator import apply_function
    """Test application of compound function."""
    assert apply_function(identity, [0]) == 0


def test_evaluate_compound(identity, fresh_env):
    """Test evaluate_compound applies function."""
    from src.evaluator import evaluate_compound
    assert evaluate_compound(identity, [0], fresh_env) == 0


def test_evaluate_compound_evaluate_identity(fresh_env):
    """Test evaluate_compound evaluates a function."""
    from src.evaluator import evaluate_compound
    op = evaluate_compound('lambda', [['x'], 'x'], fresh_env)
    assert evaluate_compound(op, [0], fresh_env) == 0


def test_evaluate_evaluates_compounds(fresh_env):
    """Test evaluate correctly evaluates compound expressions."""
    from src.evaluator import evaluate
    assert evaluate([['lambda', ['x'], 'x'], 0], fresh_env) == 0


def test_primitive_function(primitive_min):
    """Test application of primitive function.

    Primitive functions are functions which are coded in Python. This
    is analogous to functions written in C in Python."""
    from src.evaluator import apply_function
    assert apply_function(primitive_min, [1, 2]) == 1


def test_primitive_function_not_enough_args(primitive_min):
    """Test primitive_function raises TypeError for less than enough args."""
    from src.evaluator import apply_function
    with pytest.raises(TypeError):
        apply_function(primitive_min, [1])


def test_primitive_function_too_many_args(primitive_min):
    """Test primitive_function raises TypeError for more than enough args."""
    from src.evaluator import apply_function
    with pytest.raises(TypeError):
        apply_function(primitive_min, [1, 2, 3])


def test_compound_begin(fresh_env):
    """Test begin returns argument."""
    from src.evaluator import evaluate_compound
    assert evaluate_compound('begin', [1], fresh_env) == 1


def test_compound_begin_returns_last_arg(fresh_env):
    """Test begin returns argument."""
    from src.evaluator import evaluate_compound
    assert evaluate_compound('begin', [1, 2], fresh_env) == 2


def test_evaluate_lambda(fresh_env):
    """Test evaluate_lambda returns closure."""
    from src.evaluator import evaluate_lambda, evaluate
    op = evaluate_lambda([['x'], 'x'], fresh_env)
    assert evaluate([op, 0], fresh_env) == 0


def test_evaluate_begin(fresh_env):
    """Test evaluate_begin sequences expressions."""
    from src.evaluator import evaluate_begin
    assert evaluate_begin([0, 1], fresh_env) == 1


def test_evaluate_definition(fresh_env):
    """Test evaluate_definition alters the environment."""
    from src.evaluator import evaluate_definition, env_lookup
    evaluate_definition(['x', 0], fresh_env)
    assert env_lookup(fresh_env, 'x') == 0


def test_evaluate_if_true(fresh_env):
    """Test evaluate_if returns second param when first is True."""
    from src.evaluator import evaluate_if
    assert evaluate_if([True, 0, 1], fresh_env) == 0


def test_evaluate_if_false(fresh_env):
    """Test evaluate_if returns second param when first is True."""
    from src.evaluator import evaluate_if
    assert evaluate_if([False, 0, 1], fresh_env) == 1


def test_set_sets_var():
    """Test evaluate_set reassigns variable."""
    from src.evaluator import make_env, evaluate_set, env_lookup
    env = make_env({'a': 0})
    evaluate_set(['a', 1], env)
    assert env_lookup(env, 'a') == 1


def test_lookup_frame():
    """Test basic environment frame lookup."""
    from src.evaluator import make_env, lookup_frame
    assert lookup_frame(make_env({'a': 0}), 'a')['a'] == 0


def test_lookup_frame_deep():
    """Test deep environment frame lookup."""
    from src.evaluator import make_env, lookup_frame, env_extend
    env = env_extend({'a': 1}, make_env({'b': 0}))
    assert lookup_frame(env, 'b')['b'] == 0
