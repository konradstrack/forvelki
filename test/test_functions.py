from forvelki.expression.datatype import function
from forvelki.expression.misc import needs
from forvelki.parser import parser
import unittest


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


class TestArgsClosure(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		a = 1
		fun = [b; c=a -> b+c]
		a = 2
		fun(a)
		""")
	
	def testAST(self):
		fun = self.pgm[1].value
		self.assertEquals(function, type(fun))
		self.assertEquals(set(['a']), needs(fun))

	def testName(self):
		self.assertEquals([3], list(self.pgm.execute()))


class TestFunctionAssignments(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		z=0
		f = [x,y; z=z+x+y; w=z*z -> w]
		buf = f(2,3)
		buf
		""")
	
	def testNeeds(self):
		fun = self.pgm[1].value
		self.assertEquals(function, type(fun))
		self.assertEquals(set('z'), needs(fun))
	
	def testResult(self):
		self.assertEquals([25], list(self.pgm.execute()))

class TestGCD(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		gcd = f[a,b -> if b>0 then f(b,a%b) else a]
		gcd(6,9)
		gcd(1010,73)
		""")
	
	def testNeeds(self):
		fun = self.pgm[0].value
		self.assertEquals(function, type(fun))
		self.assertEquals(set(), needs(fun))

	def testResult(self):
		self.assertEquals([3, 1], list(self.pgm.execute()))


class TestFunctionPassing(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		sqr = [x -> x*x]
		apply = [fun, arg -> fun(arg)]
		apply(sqr, 5)
		""")

	def testResult(self):
		self.assertEquals([25], list(self.pgm.execute()))
		
if __name__ == "__main__":
	unittest.main()