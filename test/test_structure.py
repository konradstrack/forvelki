from forvelki.expression.misc import needs
from forvelki.parser import parser
import unittest
from forvelki.expression.datatype import identifier


class TestSimpleStructure(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		s = {x:4, y:5}
		s . x
		s . y
		{q:s}.q.y
		""")
	
	def testNeeds(self):
		self.assertEquals(set(), needs(self.pgm[0].value))

	def testResult(self):
		self.assertEquals([4,5,5], list(self.pgm.execute()))

class TestInfiniteStructure(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		enum = e[n -> {hd:n, tl:e(n+1)}]
		list = enum(1)
		list.hd
		list.tl.tl.hd
		[l -> l.tl.hd](list)
		""")

	def testResult(self):
		self.assertEquals([1,3,2], list(self.pgm.execute()))

class TestAddInfiniteBinaryTree(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		bt1 = f[n-> {val:n, left:f(2*n), right:f(2*n+1)}](1)
		bt2 = f[-> {myk:123, val:100, left:f(), right:f()}]()
		bt2.left.right.left.left.val
		bt1.right.val
		
		bt3 = add[a,b -> {val:a. val+b .val, left:add(a.left, b.left), right:add(a.right, b.right)}](bt1, bt2)
		bt3.left.right.val
		""")

	def testResult(self):
		self.assertEquals([100, 3, 105], list(self.pgm.execute()))

class TestLength(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		sum = sum[l -> if l == Empty then 0 else l.hd + sum(l.tl)]
		list = {hd:1, tl:{hd:2, tl:Empty}}
		sum(Empty)
		sum(list)
		""")

	def testResult(self):
		self.assertEquals([0,3], list(self.pgm.execute()))

class TestStrings(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		l = "ab"; l
		a = l.hd; a
		b = l.tl; b
		b.tl
		""")

	def testResult(self):
		self.assertEquals(["ab", "a", "b", identifier("Null")], list(self.pgm.execute()))

class TestStringLength(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		len = f[s-> if s==Null then 0 else 1+f(s.tl)]
		len("")
		len("foo")
		s = "mam" + "kota"
		s
		len(s)
		""")

	def testResult(self):
		self.assertEquals([0, 3, "mamkota", 7], list(self.pgm.execute()))

class TestFieldUpdate(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		s = {x:1, y:4}
		s.y
		s.x = 2
		s.x
		s.y
		o = {}
		o.f = s
		o.f.x
		o.f.y = 3
		o.f.y
		s.y
		""")

	def testResult(self):
		self.assertEquals([4, 2, 4, 2, 3, 4], list(self.pgm.execute()))

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()