from forvelki.parser import parser
import unittest
from forvelki.expression.datatype import identifier as id


class Test(unittest.TestCase):
	def setUp(self):
		self.pgm = parser.parse("""
		True
		False
		Lol
		if True then 1 else 0
		if False then 1 else 0
		""")

	def testResult(self):
		print list(self.pgm.execute())
		self.assertEquals([id("True"), id("False"), id("Lol"), 1, 0], list(self.pgm.execute()))



if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()