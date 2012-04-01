#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.yacc as yacc
import scanner

import program
import tree.conditional as conditional
import tree.operators as operators

tokens = scanner.tokens

precedence = (
			('left', 'ELSE'),
			('left', '+', '-'),
			('left', '/', '*'),
			('nonassoc', '!')
)

def p_program(p): 
	'''program : instruction SEPARATOR program'''
	p[3].appendleft(p[1])
	p[0] = p[3]

def p_program_empty(p):
	'''program : '''
	p[0] = program.program()

def p_instruction(p):
	'''instruction : expr'''
	p[0] = p[1] # TODO: this is a mock

def p_expr(p):
	'''expr : FLOAT
			| INTEGER
			| conditional'''
	p[0] = p[1]
	
# arithmetic

def p_expression_plus(p):
	'''expr : expr '+' expr'''
	p[0] = operators.add(p[1], p[3])

def p_expression_minus(p):
	'''expr : expr '-' expr'''
	p[0] = operators.subtract(p[1], p[3])
	
def p_expression_multiply(p):
	'''expr : expr '*' expr'''
	p[0] = operators.multiply(p[1], p[3])

def p_expression_divide(p):
	'''expr : expr '/' expr'''
	p[0] = operators.divide(p[1], p[3])
	
def p_negate(p):
	'''expr : '!' expr'''
	p[0] = operators.negate(p[2])
	
# conditional expressions

def p_conditional(p):
	'''conditional : IF expr THEN expr ELSE expr'''
	p[0] = conditional.conditional(p[2], p[4], p[6])
	
# errors
	
def p_error(t):
	print "Syntax error at '%s'" % t
	

parser = yacc.yacc()

if __name__ == '__main__':
	source = """if 0 then if 0 then 5 * 4 - 3 + 2 / !1 else 4 else if 1 then 2 else 3; 6;"""
	
	result = parser.parse(source)
	print result
