"""A tiny interpreter."""

from __future__ import print_function

from collections import namedtuple

try:
    input = raw_input
except NameError:
    pass


def env_extend(frame, env):
    """Extend an environment with a frame.

    frame should be dict-like."""
    return frame, env


def make_env(frame=None):
    """Return a new environment.

    If frame is specified, it is used as a top level
    environment. Otherwise, an empty environment is used."""
    return env_extend({} if frame is None else frame, None)


def lookup_frame(env, var):
    """Return first frame containing var in env."""
    while env:
        frame, env = env
        if var in frame:
            return frame
    raise KeyError('Unbound variable: {}'.format(var))


def env_lookup(env, var):
    """Look up var in environment."""
    return lookup_frame(env, var)[var]


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
    for x in expressions[:-1]:
        evaluate(x, env)
    return evaluate(expressions[-1], env)


@special_form('define')
def evaluate_definition(args, env):
    """Modify env with the new definition."""
    var, exp = args
    env[0][var] = evaluate(exp, env)


@special_form('if')
def evaluate_if(args, env):
    """Evaluate if expression."""
    exp, true, false = args
    return evaluate(true if evaluate(exp, env) else false, env)


@special_form('set!')
def evaluate_set(args, env):
    """Evaluate assignment."""
    var, exp = args
    lookup_frame(env, var)[var] = evaluate(exp, env)


def evaluate_compound(op, args, env):
    """Evaluate a compound expression."""
    special_form = isinstance(op, str) and special_forms.get(op)
    if special_form:
        return special_form(args, env)
    return apply_function(
        evaluate(op, env), [evaluate(arg, env) for arg in args]
    )


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


BUILTINS = {
    '+': primitive_function(lambda x, y: x + y, 2),
    '-': primitive_function(lambda x, y: x - y, 2),
    '*': primitive_function(lambda x, y: x * y, 2),
    '/': primitive_function(lambda x, y: x // y, 2),
    '%': primitive_function(lambda x, y: x % y, 2),
    '=': primitive_function(lambda x, y: x == y, 2),
    '<': primitive_function(lambda x, y: x < y, 2),
    '>': primitive_function(lambda x, y: x > y, 2),
    'cons': primitive_function(lambda x, y: (x, y), 2),
    'head': primitive_function(lambda p: p[0], 1),
    'tail': primitive_function(lambda p: p[1], 1),
    'null': None,
    'print': primitive_function(print, 1)
}


if __name__ == '__main__':
    from parse import read_string

    @special_form('load')
    def load(args, env):
        return evaluate(read_string(open(args[0]).read()), env)

    env = make_env(BUILTINS)
    while True:
        try:
            print(evaluate(read_string(input('[interp]> ')), env))
        except Exception:
            print('ERROR')
