def lex(s):
    """Lex a string into a list of tokens."""
    return [read_token(t) for t in
            s.replace('(', ' ( ').replace(')', ' ) ').split()]


def read_token(t):
    """Convert a token to an int if possible. Otherwise, return as is."""
    try:
        return int(t)
    except ValueError:
        return t


def parse_list(tokens):
    """Parse a list out of the tokens.

    Returns the list and an index of where that list ends."""
    res = []
    for t in tokens:
        if t == '(':
            res.append([])
        elif t == ')':
            lst = res.pop()
            if res:
                res[-1].append(lst)
            else:
                return lst
        else:
            res[-1].append(t)


def parse(tokens):
    """Turn a list of tokens into a tree of symbols and numbers."""
    t = tokens[0]
    return parse_list(tokens) if t == '(' else t


def read_string(s):
    """Parse a string."""
    return parse(lex(s))
