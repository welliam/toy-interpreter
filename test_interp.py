def test_env_lookup():
    from interp import empty_env, env_lookup, env_extend
    assert env_lookup(env_extend({'a': 0}, empty_env), 'a') == 0
