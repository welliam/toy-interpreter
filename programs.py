from interp import primitive_function, make_env


BUILTINS = {
    '+': primitive_function(lambda x, y: x + y, 2),
    '-': primitive_function(lambda x, y: x - y, 2),
    '*': primitive_function(lambda x, y: x * y, 2),
    '/': primitive_function(lambda x, y: x / y, 2),
    '%': primitive_function(lambda x, y: x % y, 2),
    '=': primitive_function(lambda x, y: x == y, 2),
    '<': primitive_function(lambda x, y: x < y, 2),
    '>': primitive_function(lambda x, y: x > y, 2),
    'cons': primitive_function(lambda x, y: (x, y), 2),
    'head': primitive_function(lambda p: p[0], 2),
    'tail': primitive_function(lambda p: p[1], 2),
    'null': None
}


env = make_env(BUILTINS)


collatz_program = [
    'begin',
    ['define', 'collatz',
     ['lambda', ['n'],
      ['if', ['=', 'n', 1],
       ['cons', 1, 'null'],
       ['cons', 'n',
        ['collatz',
         ['if', ['=', ['%', 'n', 2], 0],
          ['/', 'n', 2],
          ['+', ['*', 'n', 3], 1]]]]]]],
    ['collatz', 7]
]


overflow_the_stack = [
    'begin',
    ['define', 'overflow the stack',
     ['lambda', ['n'],
      ['if', ['=', 'n', 0],
       None,
       ['overflow the stack', ['-', 'n', 1]]]]],
    ['overflow the stack', 165]
]
