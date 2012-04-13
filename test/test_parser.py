import unittest
import forvelki.expression.conditional as conditional
import forvelki.expression.operators as operators
from forvelki.parser import parser


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
		source = "if 4 then 50 else 60;"
		
		result = parser.parse(source)
		self.assertEqual(conditional.conditional, type(result[0]))
		self.assertEqual("if(4) then(50) else(60)", repr(result[0]))