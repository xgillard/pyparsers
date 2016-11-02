'''
This module contains the tests that validate the behavior of the core
functions and classes of the pyparsers module.

Author: X. Gillard
'''
import unittest

from pyparsers import *

class TestParsers(unittest.TestCase):
    
    def setUp(self):
        self.tokens = "Bonjour tout le monde".split()
    
    # Test `text`
    def test_text_no_action(self):
        parse_txt = text("Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
    def test_text_applies_action(self):
        parse_txt = text("Bonjour", action=lambda x: x.lower())
        self.assertEqual(parse_txt(self.tokens), Success(1, "bonjour"))
        
    def test_text_not_accepted(self):
        parse_txt = text("HELLO")
        self.assertEqual(parse_txt(self.tokens), Failure(0, "Expected HELLO instead of Bonjour"))
    
    # Test `one_of`
    def test_one_of_no_action(self):
        parse_txt = one_of("Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
        parse_txt = one_of("Hello", "Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
        parse_txt = one_of("GuttenTag", "Hello", "Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
    def test_one_of_applies_action(self):
        action = lambda x: x.upper()
        parse_txt = one_of("Bonjour", action=action)
        self.assertEqual(parse_txt(self.tokens), Success(1, "BONJOUR"))
        
        parse_txt = one_of("Hello", "Bonjour", action=action)
        self.assertEqual(parse_txt(self.tokens), Success(1, "BONJOUR"))
        
        parse_txt = one_of("GuttenTag", "Hello", "Bonjour", action=action)
        self.assertEqual(parse_txt(self.tokens), Success(1, "BONJOUR"))
        
    def test_one_of_not_accepted(self):
        parse_txt = one_of("HELLO", "GuttenTag", "GoeieMorgen")
        self.assertEqual(str(parse_txt(self.tokens)), 
                         str(Failure(0, "Expecting one of the following tokens " \
                                       +"('HELLO', 'GuttenTag', 'GoeieMorgen')")))
    
    # Test `regex`
    def test_regex_no_action(self):
        parse_txt = regex(r"\w+")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
    def test_regex_applies_action(self):
        parse_txt = regex(r"\w+", action=lambda x: x.lower())
        self.assertEqual(parse_txt(self.tokens), Success(1, "bonjour"))
        
    def test_regex_not_accepted(self):
        parse_txt = regex(r"\d+")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Failure(0, "Expecting a token matching \d+")))
    
    # Test `sequence`
    def test_sequence_no_action(self):
        parse_txt = sequence("Bonjour", "tout", "le", "monde")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Success(4, ("Bonjour", "tout", "le", "monde"))))
        
        # accept another parser as argument
        parse_txt = sequence(regex(r'\w+'), 'tout', 'le', 'monde')
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Success(4, ("Bonjour", "tout", "le", "monde"))))
        
    def test_sequence_applies_action(self):
        action    = lambda bj,t,l,m: " ".join([i.upper() for i in (bj,t,l,m)])
        parse_txt = sequence("Bonjour", "tout", "le", "monde", action=action)
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Success(4, "BONJOUR TOUT LE MONDE")))
         
    def test_sequence_not_accepted(self):
        parse_txt = sequence("HELLO")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Failure(0, "Expected HELLO instead of Bonjour")))
        
        parse_txt = sequence("Bonjour", "les")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Failure(1, "Expected les instead of tout")))
    
    # Test `optional`
    def test_optional_no_action(self):
        parse_txt = optional(text("Bonjour"))
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
        parse_txt = optional(sequence("Bonjour", "tout", "le", "monde"))
        self.assertEqual(parse_txt(self.tokens), Success(4, ("Bonjour", "tout", "le", "monde")))
    
    def test_optional_applies_action_unary(self):
        action    = lambda bj: bj.upper()
        parse_txt = parse_txt = optional(text("Bonjour"), action=action)
        self.assertEqual(parse_txt(self.tokens), Success(1, "BONJOUR"))
        
    def test_optional_applies_action_multi(self):
        action    = lambda words: " ".join([i.upper() for i in words])
        parse_txt = parse_txt = optional(sequence("Bonjour", "tout", "le", "monde"), action=action)
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Success(4, "BONJOUR TOUT LE MONDE")))

    def test_optional_no_match(self):
        parse_txt = optional(text("HELLO"))
        self.assertEqual(parse_txt(self.tokens), Success(0, None))
    
    # Test `repeat`
    def test_repeat_no_min_no_max(self):
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
        
        parse_txt = repeat(regex(r'\w+'))
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
    
    def test_no_occurrence(self):
        parse_txt = repeat('GO')
        self.assertEqual(
            str(parse_txt(self.tokens)),
            str(Success(0, []))
        )
    
    def test_repeat_at_least_xtimes(self):
        # accept when matches
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=1)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
        
        # reject when not enough
        tokens    = ['GO', 'GO', 'BANG']
        parse_txt = repeat('GO', min_occurs=3)
        result    = parse_txt(tokens) 
        self.assertFalse(result.success())
        self.assertEqual(2, result.position())
        
        # reject when going off limits
        tokens    = ['GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3)
        result    = parse_txt(tokens) 
        self.assertFalse(result.success())
        self.assertEqual(2, result.position())
    
    def test_repeat_at_most_xtimes(self):
        # accept when less than max
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', max_occurs=4)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
        
        # accept when just the max
        tokens    = ['GO', 'GO', 'BANG']
        parse_txt = repeat('GO', max_occurs=2)
        result    = parse_txt(tokens) 
        self.assertEqual(result, Success(2, ['GO', 'GO']))
        
        # reject when too many matches
        tokens    = ['GO', 'GO', 'BANG']
        parse_txt = repeat('GO', max_occurs=1)
        result    = parse_txt(tokens) 
        self.assertFalse(result.success())
        self.assertEqual(2, result.position())
    
    def test_repeat_exactly_xtimes(self):
        # accept when exactly the number
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
        
        # reject when less
        tokens    = ['GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3)
        result    = parse_txt(tokens)
        self.assertEqual(2, result.position())
        self.assertFalse(result.success())
        
        # reject when too many
        tokens    = ['GO', 'GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3)
        result    = parse_txt(tokens)
        self.assertEqual(4, result.position())
        self.assertFalse(result.success())
        
    def test_repeat_applies_action(self):
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3, action=lambda x: ",".join(x))
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, "GO,GO,GO"))
        )
    
    # Test `list_of`
    def test_list_of_empty_list(self):
        "Validates that an empty list is rejected"
        parse_txt = list_of('GO')
        self.assertEqual(
            str(parse_txt(self.tokens)),
            str(Failure(0, "Expected GO instead of Bonjour"))
        )
        
    def test_list_of_nonempty_list(self):    
        tokens    = "GO , GO , GO".split()
        parse_txt = list_of('GO')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, ['GO', 'GO', 'GO']))
        )
        
    def test_list_of_custom_separator(self):    
        # accept only what uses the right separator
        tokens    = "GO , GO , GO".split()
        parse_txt = list_of('GO', '-')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(1, ['GO']))
        )
        
        tokens    = "GO * GO * GO ! GO".split()
        parse_txt = list_of('GO', '*')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, ['GO', 'GO', 'GO']))
        )
        
        # accept an other parser as param
        tokens    = "GO * GO * GO ! GO".split()
        parse_txt = list_of(regex(r'\w+'), '*')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, ['GO', 'GO', 'GO']))
        )
    
    def test_list_of_applies_action(self):    
        tokens    = "GO , GO , GO".split()
        action    = lambda xs: "-".join([x.lower() for x in xs])
        parse_txt = list_of('GO', action=action)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, 'go-go-go'))
        )
    
    # Test combinator then 
    # Test combinator +
    # Test combinator alt
    # Test combinator |
    # Test change action
    
    