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


def make_env():
    """Return a new, empty environment."""
    return ({}, None)


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


special_forms = {}


def special_form(name):
    """Name a new special form to be used by evaluate_compound."""
    def decorator(f):
        special_forms[name] = f
        return f
    return decorator


@special_form('lambda')
def evaluate_lambda(args, env):
    """Evaluate lambda expression, return compound function."""
    params, body = args
    return compound_function(params, body, env)


@special_form('begin')
def evaluate_begin(expressions, env):
    """Evaluate expressions in sequence, returning the last one."""
    for x in expressions:
        res = evaluate(x, env)
    return res


@special_form('define')
def evaluate_definition(args, env):
    """Modify env with the new definition."""
    var, exp = args
    env[0][var] = evaluate(exp, env)


def evaluate_compound(op, args, env):
    """Evaluate a compound expression."""
    special_form = isinstance(op, str) and special_forms.get(op)
    if special_form:
        return special_form(args, env)

    def evaluate_here(x):
        return evaluate(x, env)
    return apply_function(evaluate_here(op), map(evaluate_here, args))


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
