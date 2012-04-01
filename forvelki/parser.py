import ply.yacc as yacc
import scanner
import datatype

tokens = scanner.tokens

precedence = (
			('left', 'ELSE'),
			('left', 'PLUS', 'MINUS'),
			('left', 'DIVIDE', 'MULTIPLY'),
			('nonassoc', 'NEGATE')
)

def p_expr(p):
	'''expr : FLOAT
			| INTEGER
			| conditional'''
	p[0] = p[1]
	
# arithmetic

def p_expression_plus(p):
	'''expr : expr PLUS expr'''
	p[0] = datatype.add(p[1], p[3])

def p_expression_minus(p):
	'''expr : expr MINUS expr'''
	p[0] = datatype.subtract(p[1], p[3])
	
def p_expression_multiply(p):
	'''expr : expr MULTIPLY expr'''
	p[0] = datatype.multiply(p[1], p[3])

def p_expression_divide(p):
	'''expr : expr DIVIDE expr'''
	p[0] = datatype.divide(p[1], p[3])
	
def p_negate(p):
	'''expr : NEGATE expr'''
	p[0] = datatype.negate(p[2])
	
# conditional expressions

def p_conditional(p):
	'''conditional : IF expr THEN expr ELSE expr'''
	p[0] = datatype.conditional(p[2], p[4], p[6])
	
# errors
	
def p_error(t):
	print "Syntax error at '%s'" % t.value
	

parser = yacc.yacc()

if __name__ == '__main__':
	source = """if 0 then if 0 then 5 * 4 - 3 + 2 / !1 else 4 else if 1 then 2 else 3"""
	
	result = parser.parse(source)
	print result