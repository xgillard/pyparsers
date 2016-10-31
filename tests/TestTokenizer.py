'''
This module contains the tests that validate the behavior of a pyparsers.Tokenizer

Author: X. Gillard
'''
import unittest

from pyparsers import Tokenizer

class TestTokenizer(unittest.TestCase):
    
    def test_default(self):
        """
        Validates the case where the tokenizer is dumb and simply splits on 
        blank as whitespace (and nothing else)
        """
        text   = "aa,123 bb.456 cc-789"
        tested = Tokenizer()
        tokens = tested.tokenize(text)
        self.assertEqual(tokens, ["aa,123", "bb.456", "cc-789"])
        
    def test_whitespace_single(self):
        """
        Validates the behavior when the tokenizer is configured to recognize a custom marker as whitespace.
        
        Note:: Whitespace must be dropped in the tokens output
        """
        text   = "aa-123...bb-456...cc-789"
        tested = Tokenizer().whitespace(r"\.")
        tokens = tested.tokenize(text)
        self.assertEqual(tokens, ["aa-123", "bb-456", "cc-789"])
        
    def test_whitespace_multi(self):
        """
        Validates the behavior when the tokenizer is configured to recognize a complex marker as whitespace 
        (many expressions can be recognized as whitespace by the tokenizer)
        
        Note:: Whitespace must be dropped in the tokens output
        """
        text   = "aa-123.!.bb-456.!.cc-789"
        tested = Tokenizer().whitespace(r"\.", r"!")
        tokens = tested.tokenize(text)
        self.assertEqual(tokens, ["aa-123", "bb-456", "cc-789"])
        
    def test_punctuation_single(self):
        """
        Validates the behavior when the tokenizer is configured to recognize a single expression as punctuation 
        
        Note:: Punctuation must be kept in the tokens output
        """
        text   = "aa-123 bb-456 cc-789"
        tested = Tokenizer().punctuation("-")
        tokens = tested.tokenize(text)
        self.assertEqual(tokens, ["aa", "-", "123", "bb", "-", "456", "cc", "-", "789"])
    
    def test_punctuation_multi(self):
        """
        Validates the behavior when the tokenizer is configured to recognize a complex expression as punctuation
        (many sub expressions can be recognized)
        
        Note:: Punctuation must be kep in the tokens output
        """
        text   = "aa,123 bb.456 cc-789 dd.-00"
        tested = Tokenizer().punctuation("-", "\.", ",")
        tokens = tested.tokenize(text)
        self.assertEqual(tokens, ["aa", ",", "123", "bb", ".", "456", "cc", "-", "789", "dd", ".", "-", "00"])