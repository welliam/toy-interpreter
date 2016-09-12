def lex(s):
    """Lex a string into a list of tokens."""
    return [read_token(t) for t in
            s.replace('(', ' ( ').replace(')', ' ) ').split()]


def read_token(t):
    """Convert a token to a int if possible. Otherwise, return as is."""
    try:
        return int(t)
    except ValueError:
        return t


def parse_list(tokens, i):
    """Parse a list out of the tokens.

    Returns the list and an index of where that list ends."""
    todo = []
    res = []
    while True:
        t = tokens[i]
        if t == '(':
            todo.append(res)
            res = []
        elif t == ')':
            if todo:
                res = todo.pop() + [res]
            else:
                return res
        else:
            res.append(t)
        i += 1


def parse(tokens):
    """Turn a list of tokens into a tree of symbols and numbers."""
    t = tokens[0]
    return parse_list(tokens, 1) if t == '(' else t


def read_string(s):
    """Parse a string."""
    return parse(lex(s))
