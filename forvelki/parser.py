#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from expression.datatype import variable, conditional, function, invocation
from forvelki.error import BadSyntax
from forvelki.expression.datatype import structure, field_access, field_update
from program import assignment, ast as program
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


def p_possible_newlines(p):
	'''pos_nl :
			  | SEPARATOR pos_nl'''


# assignments
#def p_assignment_normal(p):
#	'''assignment : NAME '=' expr'''
#	p[0] = assignment(p[1], p[3])

def p_assignment(p):
	'''assignment : field_list '=' expr'''
#	if len(p[1]) == 1:
#		p[0] = assignment(p[1][0], p[3])
#	else:
	struct_name = p[1].popleft()
	p[0] = assignment(struct_name, field_update(variable(struct_name), p[1], p[3]))


def p_field_list(p):
	'''field_list : NAME '.' field_list'''
	p[3].appendleft(p[1])
	p[0] = p[3]

def p_field_list_end(p):
	'''field_list : NAME'''
	p[0] = deque([p[1]])

# assignment list

def p_assignment_list_empty(p):
	'''assignment_list : pos_nl'''
	p[0] = deque([])

def p_assignment_list_normal(p):
	'''assignment_list : SEPARATOR pos_nl assignment assignment_list '''
	p[4].appendleft(p[3])
	p[0] = p[4]



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
	'''key_value_list_tail : ',' pos_nl NAME ':' expr key_value_list_tail'''
	p[6].appendleft((p[3], p[5]))
	p[0] = p[6]


# expressions
def p_expr_maycallit(p):
	'''expr : expr0''' # expr0 is subset of expr, something you may invoke
	p[0] = p[1]

def p_expr_call(p):
	'''expr0 : expr0 '(' expr_list ')' '''
	p[0] = invocation(p[1], p[3])
	
#def p_expr_variable(p):
#	'''expr0 : NAME'''
#	p[0] = variable(p[1])

def p_expr_conditional(p):
	'''expr : IF bool_expr THEN pos_nl expr pos_nl ELSE pos_nl expr'''
	p[0] = conditional(p[2], p[5], p[9])

def p_expr_direct(p):
	'''expr0 : INTEGER
			| FLOAT
			| IDENTIFIER
			| lambda
			| named_function
			| STRING'''
	p[0] = p[1]
	
def p_expr_structure(p):
	'''expr0 : '{' pos_nl key_value_list pos_nl '}' '''
	p[0] = structure(p[3])

def p_field_access(p):
	'''expr0 : expr0 '.' NAME'''
	p[0] = field_access(p[1], p[3]) 

def p_field_access_field_list(p):
	'''expr0 : field_list'''
	struct = variable(p[1].popleft())
	fields = p[1]
	while fields:
		struct = field_access(struct, fields.popleft())
	p[0] = struct

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

#def p_bool_expr_identifier(p):
#	'''bool_expr : IDENTIFIER'''
#	p[0] = p[1]
def p_bool_expr_other(p):
	'''bool_expr : expr0'''
	p[0] = p[1]

	
# errors
def p_error(t):
	raise BadSyntax("bad syntax at %s" % str(t))
	

parser = yacc.yacc()	