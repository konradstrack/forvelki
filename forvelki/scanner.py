#!/usr/bin/env python
# -*- coding: utf-8 -*-
import expression.datatype as datatype

import ply.lex as lex

reserved = {
	"if" : 'IF',
	"then" : 'THEN',
	"else" : 'ELSE',
}

tokens = [
	'INTO', 'SEPARATOR', #'SHORTCUT',  
	'INTEGER', 'FLOAT', 'STRING', 'IDENTIFIER', # literals
	'COMP_EQ', 'COMP_NEQ', 'COMP_LT', 'COMP_GT', 'COMP_LE', 'COMP_GE', # comparison operators
	'NAME',
] + list(reserved.values())

literals = '@=.,:+-*/%!()[]{}' # only single-character

t_ignore = ' \t'

t_INTO = r'->'
t_COMP_EQ = r'=='
t_COMP_NEQ = r'!='
t_COMP_LT = r'<'
t_COMP_GT = r'>'
t_COMP_LE = r'<='
t_COMP_GE = r'>='

t_ignore_COMMENT = r'\#.*'

def t_SEPARATOR(t):
	r'[;\n]+'
	t.lexer.lineno += t.value.count('\n')
	return t

def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_INTEGER(t):
	r'\d+'
	t.value = int(t.value)
	return t
	
def t_STRING(t):
	r'"[^"]*"'
	t.value = t.value[1:-1]
	return t

def t_IDENTIFIER(t):
	r'[A-Z][A-Za-z0-9_]*'
	t.value = datatype.identifier(t.value)
	return t

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
	return t


def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)


lexer = lex.lex()