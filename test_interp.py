import pytest


@pytest.fixture
def test_env():
    from interp import empty_env, env_extend
    return env_extend({'a': 1},
                      env_extend({'b': 2},
                                 env_extend({'a': 0}, empty_env)))


def test_env_lookup():
    from interp import empty_env, env_lookup, env_extend
    assert env_lookup(env_extend({'a': 0}, empty_env), 'a') == 0


def test_env_lookup_lexical(test_env):
    from interp import env_lookup
    assert env_lookup(test_env, 'a') == 1


def test_env_lookup_deep(test_env):
    from interp import env_lookup
    assert env_lookup(test_env, 'b') == 2


def test_env_lookup_failure(test_env):
    from interp import env_lookup
    with pytest.raises(KeyError):
        env_lookup(test_env, '')
