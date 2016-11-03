'''
This module contains the tests that validate the behavior of the utility
functions of the pyparsers module.

Author: X. Gillard
'''
import unittest
from pyparsers import *

class TestParsingUtils(unittest.TestCase):
    # test memoize
    def test_memoize(self):
        # This is a dramatic use of the memoize decorator: 
        # DONT use it this way, PLEAAAASEE ...  
        secret = 0
        @memoize
        def memoized(i):
            nonlocal secret
            secret += i
            return secret
        
        # this time it should return comute a new result
        # and update the secret value
        x = memoized(2)
        self.assertEqual(x, 2)
        self.assertEqual(secret, 2)
        # this time it should return comute a new result
        # and update the secret value
        y = memoized(5)
        self.assertEqual(y, 7)
        self.assertEqual(secret, 7)
        # this time it should return the memoized result
        # and avoid touching the secret value
        z = memoized(2)
        self.assertEqual(z, 2)
        self.assertEqual(secret, 7)
        # idem
        w = memoized(5)
        self.assertEqual(w, 7)
        self.assertEqual(secret, 7)
        # but it doesnt mean its blocked
        u = memoized(3)
        self.assertEqual(u, 10)
        self.assertEqual(secret, 10)
        
    # test leftrec
    # test parse_all must support raw function as input param
    def test_leftrec_allows_the_definition_of_direct_left_recursive_grammar(self):
        class Grammar:
            @leftrec
            def rule(self, tokens, position=0):
                __parse = sequence(self.rule, ',', self.rule) \
                      | "OK"
                return __parse(tokens, position)
            
            def parse(self, text):
                return parse_all(text, self.rule, Tokenizer(punctuation=","))
             
        result = Grammar().parse("OK, OK, OK") 
        self.assertEqual(str(result), str( ('OK', ',', ('OK', ',', 'OK')) ))
    
    
    def test_leftrec_allows_the_definition_of_indirect_left_recursive_grammar(self):
        class Grammar:
            @leftrec
            def rule_1(self, tokens, position=0):
                __parse = sequence(self.rule_2, ',', self.rule_1) \
                      | "OK"
                return __parse(tokens, position)
            
            def rule_2(self, tokens, position):
                return self.rule_1(tokens, position)
            
            def parse(self, text):
                return parse_all(text, self.rule_1, Tokenizer(punctuation=","))
             
        result = Grammar().parse("OK, OK, OK") 
        self.assertEqual(str(result), str( ('OK', ',', ('OK', ',', 'OK')) ))