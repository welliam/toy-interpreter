def lex(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()
