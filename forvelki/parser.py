#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from expression.datatype import variable, conditional, function, invocation
from program import assignment, program
import expression.operators as operators
import ply.yacc as yacc
import scanner
from forvelki.error import BadSyntax
from forvelki.expression.datatype import structure, field_access, identifier


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


def p_possible_newlines(p):
	'''pos_nl : 
						| SEPARATOR pos_nl'''


# assignments
def p_assignment_normal(p):
	'''assignment : NAME '=' expr'''
	p[0] = assignment(p[1], p[3])


# assignment list

def p_assignment_list_empty(p):
	'''assignment_list : '''
	p[0] = deque([])

def p_assignment_list_normal(p):
	'''assignment_list : SEPARATOR assignment assignment_list '''
	p[3].appendleft(p[2])
	p[0] = p[3]



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
	'''lambda : '[' args_list assignment_list pos_nl INTO pos_nl expr pos_nl ']' '''
	p[0] = function(None, p[2], p[3], p[7])
	
def p_named_function(p):
	'''named_function : NAME '[' args_list assignment_list pos_nl INTO pos_nl expr pos_nl ']' '''
	p[0] = function(p[1], p[3], p[4], p[8])


# expression list for function invocation

def p_expr_list_empty(p):
	'''expr_list : '''
	p[0] = deque([])

def p_expr_list_normal(p):
	'''expr_list : expr expr_list_tail'''
	p[2].appendleft(p[1])
	p[0] = p[2]

def p_expr_list_tail_empty(p):
	'''expr_list_tail : '''
	p[0] = deque([])

def p_expr_list_tail_normal(p):
	'''expr_list_tail : ',' expr expr_list_tail'''
	p[3].appendleft(p[2])
	p[0] = p[3]
	
# key-value list for structure
def p_key_value_list_empty(p):
	'''key_value_list : '''
	p[0] = deque()

def p_key_value_list_normal(p):
	'''key_value_list : NAME ':' expr key_value_list_tail'''
	p[4].appendleft((p[1], p[3]))
	p[0] = p[4]

def p_key_value_list_tail_empty(p):
	'''key_value_list_tail : '''
	p[0] = deque()

def p_key_value_list_tail_normal(p):
	'''key_value_list_tail : ',' NAME ':' expr key_value_list_tail'''
	p[5].appendleft((p[2], p[4]))
	p[0] = p[5]


# expressions
def p_expr_maycallit(p):
	'''expr : expr0''' # expr0 is subset of expr, something you may invoke
	p[0] = p[1]

def p_expr_call(p):
	'''expr0 : expr0 '(' expr_list ')' '''
	p[0] = invocation(p[1], p[3])
	
def p_expr_variable(p):
	'''expr0 : NAME'''
	p[0] = variable(p[1])

def p_expr_conditional(p):
	'''expr : IF bool_expr THEN expr ELSE expr'''
	p[0] = conditional(p[2], p[4], p[6])

def p_expr_direct(p):
	'''expr : INTEGER
			| FLOAT
			| IDENTIFIER'''
	p[0] = p[1]

def p_expr_function(p):
	'''expr0 : lambda
			 | named_function'''
	p[0] = p[1]
	
def p_expr_structure(p):
	'''expr0 : '{' key_value_list '}' '''
	p[0] = structure(p[2])

def p_field_access(p):
	'''expr0 : expr0 '.' NAME'''
	p[0] = field_access(p[1], p[3]) 

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
def p_expr_modulo(p):
	'''expr : expr '%' expr'''
	p[0] = operators.modulo(p[1], p[3])
def p_expr_negate(p):
	'''expr : '!' expr'''
	p[0] = operators.negate(p[2])
def p_expr_paren(p):
	'''expr0 : '(' expr ')' '''
	p[0] = p[2]


# boolean expressions
def p_bool_expr_eq(p):
	'''bool_expr : expr COMP_EQ expr'''
	p[0] = operators.eq(p[1], p[3])
def p_bool_expr_neq(p):
	'''bool_expr : expr COMP_NEQ expr'''
	p[0] = operators.neq(p[1], p[3])
def p_bool_expr_lt(p):
	'''bool_expr : expr COMP_LT expr'''
	p[0] = operators.lt(p[1], p[3])
def p_bool_expr_gt(p):
	'''bool_expr : expr COMP_GT expr'''
	p[0] = operators.gt(p[1], p[3])
def p_bool_expr_le(p):
	'''bool_expr : expr COMP_LE expr'''
	p[0] = operators.le(p[1], p[3])
def p_bool_expr_ge(p):
	'''bool_expr : expr COMP_GE expr'''
	p[0] = operators.ge(p[1], p[3])
def p_bool_expr_expr(p): #TODO: remove
	'''bool_expr : expr'''
	p[0] = p[1]
	
# errors
	
def p_error(t):
	print "Syntax error at '%s'" % t
	raise BadSyntax
	

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
	