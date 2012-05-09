'''
Created on 09-05-2012

@author: pog
'''
from forvelki.parser import parser
import unittest


class Test(unittest.TestCase):


	def setUp(self):
		self.pgm = parser.parse("silnia = f[n -> if n>1 then (n*f(n-1)) else 1]; silnia(5); silnia(4);")

	def testName(self):
		self.assertEquals([120, 24], list(self.pgm.execute()))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()