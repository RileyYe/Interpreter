#! /usr/bin/env python
# coding=utf-8
import ply.yacc as yacc
from py_lex import *
from node import Node, num_node
from util import clear_text


# YACC for parsing Python

def simple_node(t, name):
    t[0] = Node(name)
    for i in range(1, len(t)):
        t[0].add(Node(t[i]))
    return t[0]


def p_program(t):
    '''program : statements'''
    if len(t) == 2:
        t[0] = Node('[PROGRAM]')
        t[0].add(t[1])


def p_statements(t):
    '''statements : statements statement
                  | statement'''
    t[0] = Node('[STATEMENTS]')
    if len(t) == 3:
        t[0].add(t[1])
        t[0].add(t[2])
    elif len(t) == 2:
        t[0] = t[1]


def p_statement(t):
    ''' statement : assignment
                  | print
                  | if
                  | while
                  | break
                  | for
                  | fn
                  | ret
                  | invoke
                  | class
                  | visit
'''
    if len(t) == 2:
        t[0] = Node('[STATEMENT]')
        t[0].add(t[1])

def p_visit(t):
    ''' visit : VARIABLE '.' VARIABLE'''
    t[0] = Node('[VISIT]')
    t[0].add(Node(t[1]))
    t[0].add(Node(t[3]))

def p_class(t):
    ''' class : CLASS VARIABLE '{' statements '}' '''
    t[0] = Node('[CLASS]')
    t[0].add(Node(t[2]))
    t[0].add(t[4])

def p_if(t):
    '''if : IF '(' condition ')' '{' statements '}' elseif '''
    t[0] = Node('[IF]')
    t[0].add(t[3])
    t[0].add(t[6])
    t[0].add(t[8])


def p_elseif(t):
    '''elseif :   ELIF '(' condition ')' '{' statements '}' elseif
            |   else'''
    t[0] = Node('[ELSEIF]')
    if len(t) > 2:
        t[0].add(t[3])
        t[0].add(t[6])
        t[0].add(t[8])
    else:
        t[0].add(t[1])


def p_else(t):
    '''else :   ELSE '{' statements '}'
            |   empty'''
    t[0] = Node('[ELSE]')
    if len(t) > 2:
        t[0].add(t[3])


def p_while(t):
    '''while : WHILE '(' conditions ')' '{' statements '}' '''
    t[0] = Node('[WHILE]')
    t[0].add(t[3])
    t[0].add(t[6])


def p_for(t):
    '''for : FOR '(' assignment ';' conditions ';' assignment ')' '{' statements '}' '''
    t[0] = Node('[FOR]')
    t[0].add(t[3])
    t[0].add(t[5])
    t[0].add(t[7])
    t[0].add(t[10])


def p_conditions(t):
    '''conditions :     condition
                    |   condition AND condition'''
    t[0] = Node('[CONDITIONS]')
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 4:
        t[0].add(t[1])
        t[0].add(Node(t[2]))
        t[0].add(t[3])


def p_condition(t):
    '''condition : variable LEQ variable
                    |   variable '<' variable
                    |   variable '>' variable
                    |   variable GEQ variable
                    |   variable EQ variable
                    |   variable NEQ variable'''
    t[0] = Node('[CONDITION]')
    t[0].add(t[1])
    t[0].add(Node(t[2]))
    t[0].add(t[3])


def p_break(t):
    '''break : BREAK'''
    t[0] = Node('[BREAK]')
    t[0].add(Node(t[1]))


def p_expr(t):
    '''expr : expr '+' term
            | expr '-' term
            | term'''
    t[0] = Node('[EXPR]')
    if len(t) == 4:
        t[0].add(t[1])
        t[0].add(Node(t[2]))
        t[0].add(t[3])
    else:
        t[0] = t[1]


def p_term(t):
    '''term : term '*' factor
            | term '/' factor
            | term IDIV factor
            | factor'''
    t[0] = Node('[TERM]')
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0].add(t[1])
        t[0].add(Node(t[2]))
        t[0].add(t[3])


def p_factor(t):
    '''factor : variable
                | '(' expr ')' '''
    t[0] = Node('[FACTOR]')
    if len(t) == 2:
        if isinstance(t[1], str):
            t[0].add(Node(t[1]))
        else:
            t[0] = t[1]
    else:
        t[0] = t[2]

def p_return(t):
    '''ret :    RETURN VARIABLE
            |   RETURN '''
    t[0] = Node('[RETURN]')
    if len(t) == 3:
        t[0].add(Node(t[2]))
    else:
        pass

def p_variable(t):
    '''variable :   VARIABLE '[' variable ']'
                |   VARIABLE
                |   NUMBER
                |   STR
                |   visit
    '''
    if len(t) == 2:
        t[0] = Node('[VARIABLE]')
        if isinstance(t[1], str):
            t[0].add(Node(t[1]))
        else:
            t[0] = t[1]
    else:
        t[0] = Node('[VARIABLE]')
        t[0].add(Node(t[1]))
        t[0].add(t[3])


def p_assignment(t):
    '''assignment :     variable '=' expr
                    |   variable '=' '[' agg ']'
                    |   variable '=' LEN '(' VARIABLE ')'
                    |   variable '=' VARIABLE '[' VARIABLE ']'
                    |   variable '=' VARIABLE '(' agg ')'
    '''
    if len(t) == 4:
        t[0] = Node('[ASSIGNMENT]')
        t[0].add(t[1])
        t[0].add(Node(t[2]))
        t[0].add(t[3])
    elif len(t) == 6:
        t[0] = Node('[ASSIGNMENT]')
        t[0].add(t[1])
        t[0].add(Node(t[2]))
        t[0].add(t[4])
    elif len(t) == 7:
        t[0] = Node('[ASSIGNMENT]')
        t[0].add(t[1])
        t[0].add(Node(t[2]))
        if isinstance([5], str):
            t[0].add(Node(t[3]))
            t[0].add(Node(t[5]))
        else:
            t[0].add(Node('[CLASS]'))
            t[0].add(Node(t[3]))
            t[0].add(t[5])



    else:
        t[0] = Node('[ASSIGNMENT]')
        t[0].add(t[1])
        t[0].add(Node(t[2]))
        t[0].add(Node(t[3]))
        t[0].add(Node(t[5]))


def p_agg(t):
    '''agg : VARIABLE agg
                | STR agg
                | NUMBER agg
                | ',' agg
                | VARIABLE
                | NUMBER
                | STR
                | empty '''
    t[0] = Node('[AGGREGATION]')
    if t[1] == ',':
        t[0] = t[2]
    elif len(t) == 2:
        t[0].add(Node(t[1]))
    elif len(t) == 3:
        t[0].add(Node(t[1]))
        t[0].add(t[2])
    # elif len(t) == 4:
    #     t[0].add(node(t[1]))
    #     t[0].add(node(t[2]))
    #     t[0].add(t[3])

def p_print(t):
    '''print : PRINT '(' agg ')' '''
    if len(t) == 5:
        t[0] = Node('[PRINT]')
        t[0].add(Node(t[1]))
        t[0].add(Node(t[2]))
        t[0].add(t[3])
        t[0].add(Node(t[4]))

def p_fn(t):
    '''fn : DEF VARIABLE '(' agg ')' '{' statements '}' '''
    t[0] = Node('[FUNCTION]')
    t[0].add(Node(t[2]))
    t[0].add(t[4])
    t[0].add(t[7])


def p_invoke(t):
    '''invoke : VARIABLE '(' agg ')'
            |   VARIABLE '.' VARIABLE '(' agg ')' '''
    t[0] = Node('[INVOKE]')

    if len(t) == 5:
        t[0].add(Node(t[1]))
        t[0].add(t[3])
    else:
        t[0].add(Node(t[3]))
        t[0].add(t[5])

def p_error(t):
    print("Syntax error at '%s'" % t.value)


def p_empty(t):
    '''empty : '''
    pass


yacc.yacc()
