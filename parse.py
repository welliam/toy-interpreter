def lex(s):
    """Lex a string into a list of tokens."""
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens):
    """Turn a list of tokens into a tree of symbols and numbers."""
    t = tokens[0]
    return parse_list(t) if t == '(' else t
