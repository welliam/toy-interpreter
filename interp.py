from __future__ import print_function

from evaluator import evaluate, make_env, primitive_function, special_form
from parse import read_string


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


def paren_input(prompt):
    """Reads input from stdin until parentheses are balanced."""
    result = ''
    print(prompt, end='')
    while True:
        result += input() + '\n'
        if result.strip() and balanced(result):
            return result


@special_form('load')
def load(args, env):
    return evaluate(read_string(open(args[0]).read()), env)


if __name__ == '__main__':
    env = make_env(BUILTINS)
    while True:
        try:
            print(evaluate(read_string(paren_input('[interp]> ')), env))
        except Exception as e:
            print('ERROR', e)
