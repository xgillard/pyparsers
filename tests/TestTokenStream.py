'''
This module contains the tests that validate the behavior of a pyparsers.TokenStream.

Note:: 
    The tests in here are fairly dumb given that we want the TokenStream to behave
    just like the underlying array does.

Author: X. Gillard
'''
import unittest

from pyparsers import Tokenizer, TokenStream

class TestTokenStream(unittest.TestCase):
    
    def setUp(self):
        """
        Creates a simple tokenizer
        """
        self.text      = "Hello , World !"
        self.tokenizer = Tokenizer()
        self.tokens    = self.tokenizer.tokenize(self.text)
        self.stream    = TokenStream(self.tokenizer, self.text)
        
    def test_len(self):
        "Validates that the len(..) function is coherent with underlying array"
        self.assertEqual(len(self.stream), len(self.tokens))
        
    def test_getitem_positive_idx(self):
        """
        Validates that the values returned by the [.] operator is the same as 
        that of the underlying array when the indices are meaningful (and positive)
        """
        for i in range(len(self.tokens)):
            self.assertEqual(self.stream[i], self.tokens[i])
            
    def test_getitem_negative_idx(self):
        """
        Validates that the values returned by the [.] operator is the same as 
        that of the underlying array when the indices are negative (doesn't make much
        sense in this particular case, but that's what one woudl expect anyway).
        """    
        self.assertEqual(self.stream[-1], self.tokens[-1])
    
    def test_getitem_out_of_range_idx(self):
        """
        Validates that an IndexError is raised when an incorrect position is requested
        from the stream.
        """
        self.assertRaises(IndexError, lambda : self.tokens[100])
        
    def test_contains(self):
        "Validates that the 'in' operator is consistent with that of the underlying array"
        # postive when in
        self.assertTrue("Hello" in self.stream)
        self.assertTrue("World" in self.stream)
        # negative when in
        self.assertFalse("Hello" not in self.stream)
        self.assertFalse("World" not in self.stream)
        
        # positive when not in
        self.assertFalse("Bonjour" in self.stream)
        self.assertFalse("Monde" in self.stream)
        # negative when not in
        self.assertTrue("Bonjour" not in self.stream)
        self.assertTrue("Monde" not in self.stream)
        
    def test_iter(self):
        "Validates that the iterator is consistent with that of the underlying array"
        self.assertEqual([x for x in self.stream], self.tokens)