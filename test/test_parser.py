import unittest
import forvelki.datatype as datatype
from forvelki.parser import parser

class TestParser(unittest.TestCase):
	
	def test_arithmetic(self):
		source = "5*4+3"
		
		result = parser.parse(source)

		self.assertEqual(datatype.add, type(result))
		self.assertEqual(datatype.multiply, type(result.v1))

	def test_arithmetic_repr(self):
		source = "5*4+3-2/1"
		
		expected = "5 * 4 + 3 - 2 / 1"
		result = parser.parse(source)
		
		self.assertEqual(expected, repr(result))
