empty_env = None


def env_extend(frame, new_env):
    """Extend an environment with a frame.

    frame should be dict-like."""
    return (frame, new_env)


def env_lookup(env, var):
    """Look up var in environment."""
    while env:
        frame, env = env
        try:
            return frame[var]
        except KeyError:
            pass
    raise KeyError('Unbound variable error')