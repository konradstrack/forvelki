import unittest
from forvelki.scanner import lexer

class TestLexer(unittest.TestCase):
    
    def test_comparison(self):
        source = "2 < 3"
        
        lexer.input(source)
        tokens = [token.type for token in lexer]
        
        expected = ['INTEGER', 'COMP_LT', 'INTEGER']
        self.assertListEqual(expected, tokens)