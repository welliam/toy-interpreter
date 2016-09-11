def lex(s):
    """Lex a string into a list of tokens."""
    return s.replace('(', ' ( ').replace(')', ' ) ').split()
