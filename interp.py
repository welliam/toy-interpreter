"""A tiny interpreter.

This interpreter is lexically scoped and supports functions in Python
as well as compound functions. It follows SICP's design of a mutually
recursive "eval" and "apply" (here, as "evaluate" and
"apply_function") for terseness. It is not particularly Pythonic and
sufficiently large expressions can blow the stack. I could rewrite it
iteratively using a stack, but that would be less clear (and this is a
toy anyway).

It accepts expressions written as lists. That is to say, it is not a
lexer and parser. This file does not contain an environment of
builtins, so it's not particularly usable."""


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
    """Evaluate expression under an environment. """
    if isinstance(x, list):
        return evaluate_compound(x[0], x[1:], env)
    elif isinstance(x, str):
        return env_lookup(env, x)
    return x


def evaluate_compound(op, args, env):
    """Evaluate a compound expression."""
    if op == 'lambda':
        params, body = args
        return compound_function(params, body, env)
    def ev(x):
        return evaluate(x, env)
    return apply_function(ev(op), map(ev, args))


primitive_function = namedtuple('primitive_function', 'f, arity')

compound_function = namedtuple('compound_function', 'params, body, env')


def apply_function(f, args):
    """Apply function to arguments."""
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
