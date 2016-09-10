import pytest


@pytest.fixture
def empty_env():
    from interp import env
    return env(None)


def test_env_lookup(empty_env):
    from interp import env_lookup, env_extend
    assert env_lookup(env_extend({'a': 0}, empty_env), 'a') == 0
