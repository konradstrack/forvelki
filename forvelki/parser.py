#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from expression.datatype import function
from expression.misc import variable, conditional
from forvelki.expression.datatype import call
from program import assignment, program
import expression.operators as operators
import ply.yacc as yacc
import scanner


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


# assignment list

def p_assignment_list_empty(p):
	'''assignment_list : '''
	p[0] = deque([])

def p_assignment_list_normal(p):
	'''assignment_list : SEPARATOR assignment assignment_list '''
	p[3].appendleft(p[2])
	p[0] = p[3]

#def p_assignment_list_rest_normal(p):
#	'''assignment_list_rest : assignment SEPARATOR assignment_list_rest'''
#	p[3].appendleft(p[1])
#	p[0] = p[3]	
#
#def p_assignment_list_rest_empty(p):
#	'''assignment_list_rest : '''
#	p[0] = deque([])


# functions
def p_args_list_empty(p):
	'''args_list : '''
	p[0] = deque([])

def p_args_list_normal(p):
	'''args_list : NAME rest_args_list'''
	p[2].appendleft(p[1])
	p[0] = p[2]

def p_rest_args_list_empty(p):
	'''rest_args_list : '''
	p[0] = deque([])

def p_rest_args_list_normal(p):
	'''rest_args_list : ',' NAME rest_args_list'''
	p[3].appendleft(p[2])
	p[0] = p[3]
	

def p_lambda(p):
	'''lambda : '[' args_list assignment_list INTO expr ']' '''
	p[0] = function(p[2], p[3], p[5])
	#p[0] = function(p[2], deque([]), p[4])
	
def p_named_function(p):
	'''named_function : NAME lambda '''
	p[2].name = p[1]
	p[0] = p[2]


# expressions
def p_expr_function(p):
	'''expr : named_function'''
	p[0] = p[1]

def p_expr_lambda(p):
	'''expr : lambda'''
	p[0] = p[1]

def p_expr_variable(p):
	'''expr : NAME'''
	p[0] = variable(p[1])

def p_expr_conditional(p):
	'''expr : IF expr THEN expr ELSE expr'''
	p[0] = conditional(p[2], p[4], p[6])

def p_expr_int(p):
	'''expr : INTEGER'''
	p[0] = p[1]

def p_expr_float(p):
	'''expr : FLOAT'''
	p[0] = p[1]

def p_expr_call(p):
	'''expr : NAME '(' expr ')' '''
	p[0] = call(p[1], p[3])
	#TODO: need args list
	
# arithmetic

def p_expr_plus(p):
	'''expr : expr '+' expr'''
	p[0] = operators.add(p[1], p[3])

def p_expr_minus(p):
	'''expr : expr '-' expr'''
	p[0] = operators.subtract(p[1], p[3])
	
def p_expr_multiply(p):
	'''expr : expr '*' expr'''
	p[0] = operators.multiply(p[1], p[3])

def p_expr_divide(p):
	'''expr : expr '/' expr'''
	p[0] = operators.divide(p[1], p[3])
	
def p_expr_negate(p):
	'''expr : '!' expr'''
	p[0] = operators.negate(p[2])

def p_expr_paren(p):
	'''expr : '(' expr ')' '''
	p[0] = p[2]
	
	
# errors
	
def p_error(t):
	print "Syntax error at '%s'" % t
	

parser = yacc.yacc()


if __name__ == '__main__':
	source = """
		x=5
		z=x
		x=2
		y=3
		if z-z then y else z+y
		x*y
	"""
	
	pgrm = parser.parse(source)
	print pgrm
	print
	for result in pgrm.execute():
		print result, type(result)
	