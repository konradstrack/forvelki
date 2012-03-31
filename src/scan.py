#!/usr/bin/env python
# -*- coding: utf-8 -*-

reserved = {
	"if" : 'IF',
	"then" : 'THEN',
	"else" : 'ELSE',
}

tokens = [
	'INTO', 'SEPARATOR', #'SHORTCUT', 'ASSIGN', 'COLON', 'COMMA',  
	'INTEGER', 'FLOAT', 'CHAR', 'STRING', 'IDENTIFIER', # literals
#	'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'NEGATE', # operators
	'COMP_EQU', 'COMP_UNEQU', 'COMP_LT', 'COMP_GT', 'COMP_LE', 'COMP_GE', # comparison operators
#	'IF', 'THEN', 'ELSE', # conditional instruction
#	'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LSQBRACKET', 'RSQBRACKET', # brackets
	'COMMENT', 'NAME',
] + list(reserved.values())

literals = '@=,:+-*/!()[]{}' # only single-character

t_ignore = ' \t'

t_INTO = r'->'
t_COMP_EQU = r'=='
t_COMP_UNEQU = r'!='
t_COMP_LT = r'<'
t_COMP_GT = r'>'
t_COMP_LE = r'<='
t_COMP_GE = r'>='

t_ignore_COMMENT = r'\#.*'

def t_SEPARATOR(t):
	r'[;\n]+'
	t.lexer.lineno += t.value.count('\n')
	return t

def t_INTEGER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_CHAR(t): # todo
	r"'.*'"
	
def t_STRING(t): # todo
	r'".*"'
	return t

def t_IDENTIFIER(t): # todo
	r'[A-Z][A-Za-z0-9]*'
	return t
    
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t


if __name__ == '__main__':
	import ply.lex as lex
	source = """
	x = 2 + 3 * 4
	@fun[x,y -> x+y]
	"""
	
	lexer = lex.lex()
	lexer.input(source)
	for token in lexer:
		print token
	
	