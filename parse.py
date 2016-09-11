def lex(s):
    """Lex a string into a list of tokens."""
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def parse_list(tokens, i):
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
