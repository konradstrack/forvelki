from forvelki.expression.datatype import function
from forvelki.expression.misc import needs
from forvelki.parser import parser
import unittest
from forvelki.error import UndefinedVariable


class TestFactorial(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("silnia = f[n -> if n>1 then (n*f(n-1)) else 1]; silnia(5); silnia(4);")

	def testName(self):
		self.assertEquals([120, 24], list(self.pgm.execute()))



class TestClosure(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		n = 3
		lam = [a->n+a]
		n = 4
		lam(10)
		""")
	
	def testAST(self):
		fun = self.pgm[1].value
		self.assertEquals(function, type(fun))
		self.assertEquals(set(['n']), needs(fun))

	def testName(self):
		self.assertEquals([13], list(self.pgm.execute()))


class TestUndefinedVariable(unittest.TestCase):
	def testExpr(self):
		pgm = parser.parse("x*x;")
		self.assertRaises(UndefinedVariable, lambda: list(pgm.execute()))
	
	def testAssign(self):
		pgm = parser.parse("x=a; x*x;")
		self.assertRaises(UndefinedVariable, lambda: list(pgm.execute()))


if __name__ == "__main__":
	unittest.main()