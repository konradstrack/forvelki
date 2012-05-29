from forvelki.expression.datatype import function, variable, conditional,\
	structure
from forvelki.parser import parser
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
		source = "if True then 50 else 60;"
		
		result = parser.parse(source)
		self.assertEqual(conditional, type(result[0]))
		self.assertEqual("if(True) then(50) else(60)", repr(result[0]))
		
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
		self.assertEquals(("t", 3), (self.fun.assigns[0].name, self.fun.assigns[0].value.value))
		self.assertEquals(("q", 5.6), (self.fun.assigns[1].name, self.fun.assigns[1].value.value))
		
	
class TestNamedFunction(unittest.TestCase):
	def setUp(self):
		self.fun = parser.parse("sil[n -> if 4+3>0 then 2 else 1];")[0]
	
	def test_name(self):
		self.assertEquals("sil", self.fun.name)

class TestStructure(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("{x:4, y:5};")
	
	def testAst(self):
		self.assertEquals(structure, type(self.pgm[0]))
		self.assertEquals(structure({'y':5, 'x':4}), self.pgm[0])
	
class TestNewline(unittest.TestCase):
	def testGetsParsedCorrectly(self):
		parser.parse("""
		s = {
			x:1,
			y:2
		}
		s
		
		fun = name[x,y;
			z = x+y;
			z = z*z ->	
			z + 1
		]
		fun(1,2)
		
		lam = [a;;;;; x=1; ->	a+1;;;;;;
		]

		""")
		