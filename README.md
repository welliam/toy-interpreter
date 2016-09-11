A tiny interpreter.

This interpreter is lexically scoped and supports functions in Python
as well as compound functions. It follows SICP's design of a mutually
recursive "eval" and "apply" (here, as "evaluate" and
"apply_function") for simplicity. It is not particularly Pythonic and
sufficiently large expressions can blow the stack. I could rewrite it
iteratively using a stack, but that would be less clear (and this is
for demonstrational purposes, so clarity takes precedence).

It accepts expressions written as lists. That is to say, it is not a
lexer and parser. Such a lexer and parser could be written rather
easily, with outputs that resemble the inputs for interp.py.
