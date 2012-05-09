from forvelki.expression.datatype import function
from forvelki.expression.misc import variable
from forvelki.parser import parser
from forvelki.program import assignment
import forvelki.expression.misc as conditional
import forvelki.expression.operators as operators
import unittest

class TestParser(unittest.TestCase):
	
	def test_arithmetic(self):
		source = "5*4+3;"
		
		result = parser.parse(source)

		self.assertEqual(operators.add, type(result[0]))
		self.assertEqual(operators.multiply, type(result[0].v1))

	def test_arithmetic_repr(self):
		source = "5*4+3-2/1;"
		
		expected = '5 * 4 + 3 - 2 / 1'
		
		result = parser.parse(source)
		
		self.assertEqual(expected, repr(result[0]))

	def test_conditional_expression(self):
		source = "if 4 then 50 else 60;"
		
		result = parser.parse(source)
		self.assertEqual(conditional.conditional, type(result[0]))
		self.assertEqual("if(4) then(50) else(60)", repr(result[0]))
		
class TestSimplestFunction(unittest.TestCase):
	def setUp(self):
		self.parsed = parser.parse("[->3];")
	
	def test_ast(self):
		fun = self.parsed[0]
		self.assertEquals(function, type(fun))
		self.assertEquals(0, len(fun.args))
		self.assertEquals(0, len(fun.assigns))
		self.assertEquals(3, fun.expr)

class TestFunction(unittest.TestCase):
	def setUp(self):
		self.fun = parser.parse("""[x,y ;t=3;q=5.6 ->1+z];""")[0]
							#"""[x,y -> pam+2 ];
		#""")[0]
	
	def test_args(self):
		self.assertEquals(["x","y"], list(self.fun.args))
	
	def test_expr(self):
		self.assertEquals(str(operators.add(1, variable("z"))), str(self.fun.expr))
	
	def test_assigns(self):
		self.assertEquals(2, len(self.fun.assigns))
		self.assertEquals(assignment("t", 3), self.fun.assigns[0])
		self.assertEquals(assignment("q", 5.6), self.fun.assigns[1])
		
	
class TestNamedFunction(unittest.TestCase):
	def setUp(self):
		self.fun = parser.parse("sil[n -> if 4+3 then 2 else 1];")[0]
	
	def test_name(self):
		self.assertEquals("sil", self.fun.name)
		