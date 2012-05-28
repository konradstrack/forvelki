from forvelki.expression.datatype import function, invocation
from forvelki.expression.misc import needs
from forvelki.parser import parser
import unittest

class TestFib(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		fib = f[n -> if n<2 then 1 else f(n-2)+f(n-1)]
		fib(2); fib(3); fib(4)
		""")
	
	def testAST(self):
		self.assertEquals(invocation, type(self.pgm[1]))
		self.assertEquals([2], list(self.pgm[1].act_args))

	def testResult(self):
		self.assertEquals([2, 3, 5], list(self.pgm.execute()))

class TestFactorial(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		silnia = f[n -> if n<=1 then 1 else n*f(n-1)]
		silnia(5)
		silnia(4)
		""")
	
	def testAst(self):
		fun = self.pgm[0].value.value
		els = fun.expr.if_false
		inv = els.v2
		self.assertEquals(invocation, type(inv))

	def testResult(self):
		self.assertEquals([120, 24], list(self.pgm.execute()))



class TestClosure(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		n = 3
		lam = [a->n+a]
		n = 4
		lam(10)
		[x,y->x+y](3,5)
		""")
	
	def testAST(self):
		fun = self.pgm[1].value.value
		self.assertEquals(function, type(fun))
		self.assertEquals(set(['n']), needs(fun))

	def testResult(self):
		self.assertEquals([13,8], list(self.pgm.execute()))


class TestArgsClosure(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		a = 1
		fun = [b; c=a -> b+c]
		a = 2
		fun(a)
		""")
	
	def testAST(self):
		fun = self.pgm[1].value.value
		self.assertEquals(function, type(fun))
		self.assertEquals(set(['a']), needs(fun))

	def testResult(self):
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
		fun = self.pgm[1].value.value
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
		fun = self.pgm[0].value.value
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

class TestYCombinator(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		fixpoint = me[f -> f(me(f))]
		gf = [fun -> [n -> if n>1 then n*fun(n-1) else 1] ] # look! no recurrence.
		fixpoint(gf)(0); fixpoint(gf)(4); fixpoint(gf)(5)
		
		y = [f; lam = [x -> f(x(x))] -> lam(lam)] # hardcore Haskell Curry's fixpoint combinator
		factorial = y(gf)
		factorial(3)
		""")
	
	def testResult(self):
		self.assertEquals([1, 24, 120, 6], list(self.pgm.execute()))

class TestNestedFunctions(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		genfun = [ a,b
			addA = [n -> n+a]
			mulB = [n -> n*b] ->
			[n -> mulB(addA(n))]
		]
		fun = genfun(1,10)
		fun(3)
		""")
	
	def testResult(self):
		self.assertEquals([40], list(self.pgm.execute()))

class TestFastPower(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		pow = f[p,w; q=f(p*p,w/2) -> if (!w) then 1 else (if (w%2) then p*q else q)]
		pow(2,3)
		""")
	
	def testResult(self):
		self.assertEquals([8], list(self.pgm.execute()))
	
	

class TestBuiltinWrite(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		write(123)
		""")
	
	def testResult(self):
		self.assertEquals([123], list(self.pgm.execute()))
	
		
if __name__ == "__main__":
	unittest.main()