from forvelki.expression.misc import needs
from forvelki.parser import parser
import unittest


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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()