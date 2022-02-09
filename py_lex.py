#! /usr/bin/env python
# coding=utf-8
import ply.lex as lex
import util

# LEX for parsing Python

# Tokens
tokens = (
    'VARIABLE', 'NUMBER', 'PRINT', 'LEQ', 'GEQ', 'EQ', 'WHILE', 'IF', 'ELSE', 'ELIF', 'LEN', 'IDIV', 'BREAK', 'NEQ',
    'FOR', 'AND', 'DEF', 'RETURN', 'STR', 'CLASS')

literals = ['=', '+', '-', '*', '(', ')', '{', '}', '<', '>', ',', '*', '/', '[', ']', ';', '.']


# Define of tokens

def t_CLASS(t):
    '''class'''
    return t

def t_IDIV(t):
    """//"""
    return t


def t_RETURN(t):
    '''return'''
    return t


def t_LEQ(t):
    '<='
    return t


def t_GEQ(t):
    '>='
    return t


def t_EQ(t):
    '=='
    return t


def t_NEQ(t):
    '!='
    return t


def t_NUMBER(t):
    r'[0-9]+'
    return t


def t_WHILE(t):
    '''while'''
    return t


def t_IF(t):
    """if"""
    return t


def t_ELIF(t):
    '''elif'''
    return t


def t_ELSE(t):
    '''else'''
    return t


def t_BREAK(t):
    '''break'''
    return t


def t_DEF(t):
    '''def'''
    return t


def t_FOR(t):
    '''for'''
    return t


def t_LEN(t):
    """len"""
    return t


def t_AND(t):
    '''and'''
    return t


def t_PRINT(t):
    r'print'
    return t


def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_STR(t):
    r"""'.*'"""
    return t


# Ignored
t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
# lexer.input(util.clear_text( open('0.txt').read()))
# while True:
#     tok = lexer.token()
#     if not tok: break  # No more input
#     print(tok)
