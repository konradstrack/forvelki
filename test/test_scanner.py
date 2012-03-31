import unittest
from forvelki.scanner import lexer

class TestLexer(unittest.TestCase):
    
    def test_comparison(self):
        source = "2 < 3.5"
        
        lexer.input(source)
        tokens = [token.type for token in lexer]
        
        expected = ['INTEGER', 'COMP_LT', 'FLOAT']
        self.assertListEqual(expected, tokens)
        
    def test_brackets(self):
        source = "[{}]()"
        
        lexer.input(source)
        tokens = [token.type for token in lexer]
        
        expected = ['LSQBRACKET', 'LBRACE', 'RBRACE', 'RSQBRACKET', 'LPAREN', 'RPAREN']
        self.assertListEqual(expected, tokens)
        
    def test_operators(self):
        source = "!+*-/"
        
        lexer.input(source)
        tokens = [token.type for token in lexer]
        
        expected = ['NEGATE', 'PLUS', 'MULTIPLY', 'MINUS', 'DIVIDE']
        self.assertListEqual(expected, tokens)