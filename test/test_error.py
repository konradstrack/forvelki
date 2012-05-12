from forvelki.error import UndefinedVariable
from forvelki.parser import parser
import unittest


class TestUndefinedVariable(unittest.TestCase):
	def testExpr(self):
		pgm = parser.parse("x*x;")
		self.assertRaises(UndefinedVariable, lambda: list(pgm.execute()))
	
	def testAssign(self):
		pgm = parser.parse("x=a; x*x;")
		self.assertRaises(UndefinedVariable, lambda: list(pgm.execute()))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()