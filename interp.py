from collections import namedtuple


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
    if isinstance(x, list):
        return evaluate_compound(x[0], x[1:], env)
    elif isinstance(x, str):
        return env_lookup(env, x)
    return x


def evaluate_compound(op, args, env):
    if op == 'lambda':
        params, body = args
        return compound_function(params, body, env)
    def ev(x):
        return evaluate(x, env)
    return apply_function(ev(op), map(ev, args))


primitive_function = namedtuple('primitive_function', 'f, arity')

compound_function = namedtuple('compound_function', 'params, body, env')


def apply_function(f, args):
    if isinstance(f, primitive_function):
        f, arity = f
        if len(args) != arity:
            message = 'Arity error: expected {} args, received {}'.format(
                arity, args
            )
            raise TypeError(message)
        return f(*args)
    else:
        params, body, env = f
        new_env = env_extend(dict(zip(params, args)), env)
        return evaluate(body, new_env)
