#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.yacc as yacc
import scanner


import expression.operators as operators
from program import assignment, program
from expression.misc import variable, conditional
from expression.datatype import integer, floating

tokens = scanner.tokens

precedence = (
			('left', 'ELSE'),
			('left', '+', '-'),
			('left', '/', '*'),
			('nonassoc', '!')
)

def p_program(p): 
	'''program : instruction SEPARATOR program'''
	if p[1] is not None:
		p[3].appendleft(p[1])
	p[0] = p[3]

def p_program_empty(p):
	'''program : '''
	p[0] = program()

def p_instruction(p):
	'''instruction : expr 
				   | assignment'''
	p[0] = p[1]

def p_instruction_empty(p):
	'''instruction : '''
	p[0] = None



# assignments
def p_assignment_normal(p):
	'''assignment : NAME '=' expr'''
	p[0] = assignment(p[1], p[3])

#def p_assignment_function_shortcut(p): # TODO: later
#	'''assignment : '@' NAME lambda '''
#	p[0] = assignment()


def p_expr_variable(p):
	'''expr : NAME'''
	p[0] = variable(p[1])

def p_expr_conditional(p):
	'''expr : IF expr THEN expr ELSE expr'''
	p[0] = conditional(p[2], p[4], p[6])

def p_expr_int(p):
	'''expr : INTEGER'''
	p[0] = integer(p[1]) #TODO: error handling

def p_expr_float(p):
	'''expr : FLOAT'''
	p[0] = floating(p[1]) #TODO: error handling
	
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
	
	
# errors
	
def p_error(t):
	print "Syntax error at '%s'" % t
	

parser = yacc.yacc()

if __name__ == '__main__':
	source = """
		x=5
		y=3.14
		if x-x then y else x+y
		x=2
		x*y
	"""
	
	pgrm = parser.parse(source)
	print pgrm
	print
	for result in pgrm.execute():
		print result, type(result)
	