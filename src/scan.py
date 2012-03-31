# -*- coding: utf-8 -*-
import ply.lex as lex

tokens = (
	'INTEGER', 'FLOAT', 'CHAR', 'STRING', 'IDENTIFIER', # literals
	'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'NEGATE', # operators
	'COMP_EQU', 'COMP_UNEQU', 'COMP_LT', 'COMP_GT', 'COMP_LE', 'COMP_GE', # comparison operators
	'IF', 'THEN', 'ELSE', # conditional instruction
	'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LSQBRACKET', 'RSQBRACKET', # brackets
	'INTO', 'SHORTCUT', 'ASSIGN', 'COLON', 'COMMA', 'SEMICOLON'  # others: ->, @, =, :, ,,
)
