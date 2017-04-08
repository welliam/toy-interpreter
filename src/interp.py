from __future__ import print_function
import sys

from .evaluator import evaluate, make_env, primitive_function, special_form
from .parse import read_string

try:
    input = raw_input
except NameError:
    pass


class Null(object):
    """The empty list."""
    def __str__(self):
        return '()'


null = Null()


class Cons(tuple):
    """Cons object"""
    def __str__(self):
        last_pair = self
        while isinstance(last_pair[1], Cons):
            last_pair = last_pair[1]
        return (list_to_str if last_pair[1] is null else pair_to_str)(self)


def cons(a, b):
    """Create a cons."""
    return Cons((a, b))


def pair_to_str(pair):
    """Return a pair as a string."""
    return '({} . {})'.format(pair[0], pair[1])


def list_to_str(lst):
    """Return a list as a string."""
    res = '('
    while lst[1] is not null:
        res += '{} '.format(lst[0])
        lst = lst[1]
    return res + '{})'.format(lst[0])


BUILTINS = {
    '+': primitive_function(lambda x, y: x + y, 2),
    '-': primitive_function(lambda x, y: x - y, 2),
    '*': primitive_function(lambda x, y: x * y, 2),
    '/': primitive_function(lambda x, y: x // y, 2),
    'modulo': primitive_function(lambda x, y: x % y, 2),
    '=': primitive_function(lambda x, y: x == y, 2),
    '<': primitive_function(lambda x, y: x < y, 2),
    '>': primitive_function(lambda x, y: x > y, 2),
    '>=': primitive_function(lambda x, y: x >= y, 2),
    '<=': primitive_function(lambda x, y: x <= y, 2),
    'cons': primitive_function(cons, 2),
    'head': primitive_function(lambda p: p[0], 1),
    'tail': primitive_function(lambda p: p[1], 1),
    'null': null,
    '#f': False,
    '#t': True,
    'print': primitive_function(print, 1)
}


def balanced(s):
    """Return whether the input has balanced parentheses.

    Raises an error if too many close parentheses are in string."""
    opens = 0
    for c in s:
        if c == '(':
            opens += 1
        elif c == ')':
            if opens:
                opens -= 1
            else:
                raise ValueError('Unbalanced parens')
    return opens == 0


def paren_input(prompt, port=sys.stdin):
    """Reads input from stdin until parentheses are balanced."""
    result = ''
    print(prompt, end='')
    sys.stdout.flush()
    while True:
        result += sys.stdin.readline()
        if result.strip() and balanced(result):
            return result


@special_form('load')
def load(args, env):
    """Evaluate an entire file."""
    evaluate(read_string('(begin {})'.format(open(args[0]).read())), env)


if __name__ == '__main__':
    env = make_env(BUILTINS)
    print('Ctrl-c to exit')
    while True:
        try:
            print(evaluate(read_string(paren_input('[interp]> ')), env))
        except Exception as e:
            print('ERROR', e)
