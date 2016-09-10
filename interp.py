empty_env = None


def env_extend(frame, new_env):
    """Extend an environment with a frame.

    frame should be dict-like."""
    return frame, new_env


def env_lookup(env, var):
    """Look up var in environment."""
    while env:
        frame, env = env
        try:
            return frame[var]
        except KeyError:
            pass
    raise KeyError('Unbound variable: {}'.format(var))


def evaluate(x, env):
    if isinstance(x, str):
        return env_lookup(env, x)
    return x


def primitive_function(f, arity):
    return f, arity


def apply_function(f, args):
    f, arity = f
    if len(args) != arity:
        raise TypeError(
            'Arity error: expected {} args, received {}'.format(arity, args)
        )
    return f(*args)
