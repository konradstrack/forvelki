import ply.yacc as yacc
import scanner
import datatype

tokens = scanner.tokens

precedence = (
			('left', 'PLUS', 'MINUS'),
			('left', 'DIVIDE', 'MULTIPLY'),
)

def p_expr(p):
	'''expr : FLOAT
			| INTEGER'''
	p[0] = p[1]

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
	
def p_error(t):
	print "Syntax error at '%s'" % t.value

parser = yacc.yacc()

if __name__ == '__main__':
	source = "5 * 4 - 3 + 2 / 1"
	
	result = parser.parse(source)
	print result