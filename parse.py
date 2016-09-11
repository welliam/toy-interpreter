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
    res = []
    while True:
        t = tokens[i]
        if t == '(':
            exp, i = parse_list(tokens, i+1)
            res.append(exp)
        elif t == ')':
            return res, i + 1
        else:
            res.append(t)
            i += 1


def parse(tokens):
    """Turn a list of tokens into a tree of symbols and numbers."""
    t = tokens[0]
    return parse_list(tokens, 1)[0] if t == '(' else t
