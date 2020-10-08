#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

tokens = ( 'NAME', 'NUMBER',)

literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens
#t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def l_NUMBER(t):
#    r'\d+'
    t.value = int(t.value)
    return t

#l_ignore = " \t"

def l_newline(t):
#    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def l_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t = {
"tokens": tokens,
"literals": literals,
"t_ignore": "\t",
r'[a-zA-Z_][a-zA-Z0-9_]*': l_NAME,
r'\d+': l_NUMBER,
r'\n+': l_newline,
"t_error": l_error
}

# Build the lexer
import lex
lexer = lex.lex(module=t)

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]

#def p_statement_expr(p):
#    'statement : expression'
#    print(p[1])
#
#def p_expression_binop(p):
#    '''expression : expression '+' expression
#                  | expression '-' expression
#                  | expression '*' expression
#                  | expression '/' expression'''
#    if p[2] == '+':
#        p[0] = p[1] + p[3]
#    elif p[2] == '-':
#        p[0] = p[1] - p[3]
#    elif p[2] == '*':
#        p[0] = p[1] * p[3]
#    elif p[2] == '/':
#        p[0] = p[1] / p[3]
#
#def p_expression_uminus(p):
#    "expression : '-' expression %prec UMINUS"
#    p[0] = -p[2]
#
#def p_expression_group(p):
#    "expression : '(' expression ')'"
#    p[0] = p[2]
#
#def p_expression_number(p):
#    "expression : NUMBER"
#    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

def add(p): p[0] = p[1] + p[3]
def sub(p): p[0] = p[1] - p[3]
def mul(p): p[0] = p[1] * p[3]
def div(p): p[0] = p[1] / p[3]
def uminus(p): p[0] = -p[2]
def two(p): p[0] = p[2]
def one(p): p[0] = p[1]
p = {
"tokens": tokens,
"precedence": precedence,
"statement : NAME '=' expression": p_statement_assign,
"statement : expression": lambda p: print(p[1]),
"expression : expression '+' expression": add,
"expression : expression '-' expression": sub,
"expression : expression '*' expression": mul,
"expression : expression '/' expression": div,
"expression : '-' expression %prec UMINUS": uminus,
"expression : '(' expression ')'": two,
"expression : NUMBER": one,
"expression : NAME": p_expression_name,
"p_error": p_error
}

import yacc
parser = yacc.yacc(module=p)

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
