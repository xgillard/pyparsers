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
    def test_one_of_should_suceed_when_it_matches_sole_proposition_and_no_action_is_applied(self):
        parse_txt = one_of("Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
    
    def test_one_of_should_suceed_when_it_matches_second_of_two_propositions_and_no_action_is_applied(self): 
        parse_txt = one_of("Hello", "Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
    
    def test_one_of_should_suceed_when_it_matches_last_of_three_propositions_and_no_action_is_applied(self):
        parse_txt = one_of("GuttenTag", "Hello", "Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
    def test_one_of_applies_action_when_matching_single_proposition(self):
        action = lambda x: x.upper()
        parse_txt = one_of("Bonjour", action=action)
        self.assertEqual(parse_txt(self.tokens), Success(1, "BONJOUR"))
    
    def test_one_of_applies_action_when_matching_single_of_two_proposition(self):    
        action = lambda x: x.upper()
        parse_txt = one_of("Hello", "Bonjour", action=action)
        self.assertEqual(parse_txt(self.tokens), Success(1, "BONJOUR"))
    
    def test_one_of_applies_action_when_matching_last_of_three_proposition(self):    
        action = lambda x: x.upper()    
        parse_txt = one_of("GuttenTag", "Hello", "Bonjour", action=action)
        self.assertEqual(parse_txt(self.tokens), Success(1, "BONJOUR"))
        
    def test_one_of_not_accepted(self):
        parse_txt = one_of("HELLO", "GuttenTag", "GoeieMorgen")
        self.assertEqual(str(parse_txt(self.tokens)), 
                         str(Failure(0, "Expecting one of the following tokens " \
                                       +"('HELLO', 'GuttenTag', 'GoeieMorgen')")))
    
    # Test `regex`
    def test_regex_should_succeed_when_token_matches_pattern_and_no_action_is_given(self):
        parse_txt = regex(r"\w+")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
    def test_regex_applies_action_upon_success(self):
        parse_txt = regex(r"\w+", action=lambda x: x.lower())
        self.assertEqual(parse_txt(self.tokens), Success(1, "bonjour"))
        
    def test_regex_not_accepted(self):
        parse_txt = regex(r"\d+")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Failure(0, "Expecting a token matching \d+")))
    
    # Test `sequence`
    def test_sequence_should_succeed_when_all_tokens_appear_in_order__no_action(self):
        parse_txt = sequence("Bonjour", "tout", "le", "monde")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Success(4, ("Bonjour", "tout", "le", "monde"))))
    
    def test_sequence_should_handle_parsers_just_like_plaintext__no_action(self):    
        # accept another parser as argument
        parse_txt = sequence(regex(r'\w+'), 'tout', 'le', 'monde')
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Success(4, ("Bonjour", "tout", "le", "monde"))))
        
    def test_sequence_applies_a_variadic_action_upon_success(self):
        action    = lambda bj,t,l,m: " ".join([i.upper() for i in (bj,t,l,m)])
        parse_txt = sequence("Bonjour", "tout", "le", "monde", action=action)
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Success(4, "BONJOUR TOUT LE MONDE")))
         
    def test_sequence_should_reject_when_token_at_position_does_not_match_expectation(self):
        parse_txt = sequence("HELLO")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Failure(0, "Expected HELLO instead of Bonjour")))
    
    def test_sequence_should_reject_when_token_at_subsequent_used_position_does_not_match_expectation(self):
        parse_txt = sequence("Bonjour", "les")
        self.assertEqual(
            str(parse_txt(self.tokens)), 
            str(Failure(1, "Expected les instead of tout")))
    
    # Test `optional`
    def test_optional_should_succeed_when_text_corresponds__no_action(self):
        parse_txt = optional("Bonjour")
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
    
    def test_optional_should_succeed_when_matcher_succeeds__no_action(self):
        parse_txt = optional(text("Bonjour"))
        self.assertEqual(parse_txt(self.tokens), Success(1, "Bonjour"))
        
    def test_optional_should_succeed_when_matcher_succeeds2__no_action(self):
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

    def test_optional_should_succeed_even_when_there_is_no_match(self):
        parse_txt = optional(text("HELLO"))
        self.assertEqual(parse_txt(self.tokens), Success(0, None))
    
    # Test `repeat`
    def test_repeat_should_accept_all_matching_text_when_no_min_nor_max_is_given__no_action(self):
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
    def test_repeat_should_accept_all_parsed_tokens_when_no_min_nor_max_is_given__no_action(self):
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat(regex(r'\w+'))
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
    
    def test_repeat_should_succeed_even_when_there_are_no_occurrence_to_be_parsed__no_action(self):
        parse_txt = repeat('GO')
        self.assertEqual(
            str(parse_txt(self.tokens)),
            str(Success(0, []))
        )
    
    def test_repeat_at_least_xtimes_should_accept_tokens_when_condition_is_met(self):
        # accept when matches
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=1)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
    
    def test_repeat_at_least_xtimes_should_reject_when_there_are_not_enough_matches(self):    
        # reject when not enough
        tokens    = ['GO', 'GO', 'BANG']
        parse_txt = repeat('GO', min_occurs=3)
        result    = parse_txt(tokens) 
        self.assertFalse(result.success())
        self.assertEqual(2, result.position())
    
    def test_repeat_at_least_xtimes_must_not_fail_because_of_stream_boundaries(self):
        # reject when going off limits
        tokens    = ['GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3)
        result    = parse_txt(tokens) 
        self.assertFalse(result.success())
        self.assertEqual(2, result.position())
    
    def test_repeat_at_most_xtimes_should_accept_when_there_are_less_than_max_matches(self):
        # accept when less than max
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', max_occurs=4)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
    
    def test_repeat_at_most_xtimes_should_accept_when_there_are_exactly_max_matches(self):    
        # accept when just the max
        tokens    = ['GO', 'GO', 'BANG']
        parse_txt = repeat('GO', max_occurs=2)
        result    = parse_txt(tokens) 
        self.assertEqual(result, Success(2, ['GO', 'GO']))
    
    def test_repeat_at_most_xtimes_should_reject_when_there_are_too_many_matches(self):
        # reject when too many matches
        tokens    = ['GO', 'GO', 'BANG']
        parse_txt = repeat('GO', max_occurs=1)
        result    = parse_txt(tokens) 
        self.assertFalse(result.success())
        self.assertEqual(2, result.position())
    
    def test_repeat_exactly_xtimes_should_accept_when_there_is_the_right_number_of_matches(self):
        # accept when exactly the number
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, tokens))
        )
    
    def test_repeat_exactly_xtimes_should_reject_when_not_enough_matches(self):
        # reject when less
        tokens    = ['GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3)
        result    = parse_txt(tokens)
        self.assertEqual(2, result.position())
        self.assertFalse(result.success())
        
    def test_repeat_exactly_xtimes_should_reject_when_there_are_too_many_matches(self):
        # reject when too many
        tokens    = ['GO', 'GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3)
        result    = parse_txt(tokens)
        self.assertEqual(4, result.position())
        self.assertFalse(result.success())
        
    def test_repeat_applies_action_upon_success(self):
        tokens    = ['GO', 'GO', 'GO']
        parse_txt = repeat('GO', min_occurs=3, max_occurs=3, action=lambda x: ",".join(x))
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(3, "GO,GO,GO"))
        )
    
    # Test `list_of`
    def test_list_of_should_reject_an_empty_list(self):
        "Validates that an empty list is rejected"
        parse_txt = list_of('GO')
        self.assertEqual(
            str(parse_txt(self.tokens)),
            str(Failure(0, "Expected GO instead of Bonjour"))
        )
        
    def test_list_of_should_accept_a_nonempty_list(self):    
        tokens    = "GO , GO , GO".split()
        parse_txt = list_of('GO')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, ['GO', 'GO', 'GO']))
        )
        
    def test_list_of_must_accept_only_what_uses_the_right_separator__single_entry(self):    
        # accept only what uses the right separator
        tokens    = "GO , GO , GO".split()
        parse_txt = list_of('GO', '-')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(1, ['GO']))
        )
    
    def test_list_of_must_accept_only_what_uses_the_right_separator__multiple_matches(self):    
        tokens    = "GO * GO * GO ! GO".split()
        parse_txt = list_of('GO', '*')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, ['GO', 'GO', 'GO']))
        )
    
    def test_list_of_must_accept_an_other_parser_as_input(self):
        # accept an other parser as param
        tokens    = "GO * GO * GO ! GO".split()
        parse_txt = list_of(regex(r'\w+'), '*')
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, ['GO', 'GO', 'GO']))
        )
    
    def test_list_of_applies_action_upon_success(self):    
        tokens    = "GO , GO , GO".split()
        action    = lambda xs: "-".join([x.lower() for x in xs])
        parse_txt = list_of('GO', action=action)
        self.assertEqual(
            str(parse_txt(tokens)),
            str(Success(5, 'go-go-go'))
        )
    
    # Test combinator then
    def test_combinator_then_must_reject_when_first_token_doesnt_match(self):
        # reject when first does not match
        parse_txt = text("GO").then("GO")
        result    = parse_txt(['Bonjour', 'tout', 'le', 'monde'])
        self.assertEqual(
            str(result),
            str(Failure(0, "Expected GO instead of Bonjour")))
    
    def test_combinator_then_must_reject_when_subsequent_tokens_dont_match(self):    
        # reject when following does not match
        parse_txt = text("GO").then("GO")
        result    = parse_txt(['GO', 'wild', '!'])
        self.assertEqual(
            str(result),
            str(Failure(1, "Expected GO instead of wild")))
        
    def test_combinator_then_should_accept_when_both_token_match(self):
        # accept when both match
        parse_txt = text("GO").then("GO")
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(2, ('GO', 'GO'))))
        
    def test_combinator_then_should_accept_parser_as_argument(self):
        # accept when both match
        parse_txt = text("GO").then(regex(r"\w+"))
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(2, ('GO', 'GO'))))
    
    def test_combinator_then_should_apply_binary_action_upon_success(self):
        # accept when both match
        action    = lambda a,b: a.lower()+","+b.lower()
        parse_txt = text("GO").then("GO", action=action)
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(2, "go,go")))
        
    # Test combinator +
    def test_operator_PLUS_must_reject_when_first_token_doesnt_match(self):
        # reject when first does not match
        parse_txt = text("GO") + "GO"
        result    = parse_txt(['Bonjour', 'tout', 'le', 'monde'])
        self.assertEqual(
            str(result),
            str(Failure(0, "Expected GO instead of Bonjour")))
    
    def test_operator_PLUS_must_reject_when_subsequent_tokens_dont_match(self):    
        # reject when following does not match
        parse_txt = text("GO") + "GO"
        result    = parse_txt(['GO', 'wild', '!'])
        self.assertEqual(
            str(result),
            str(Failure(1, "Expected GO instead of wild")))
        
    def test_operator_PLUS_should_accept_when_both_token_match(self):
        # accept when both match
        parse_txt = text("GO") + "GO"
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(2, ('GO', 'GO'))))
        
    def test_operator_PLUS_should_accept_parser_as_argument(self):
        # accept when both match
        parse_txt = text("GO") + regex(r"\w+")
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(2, ('GO', 'GO'))))
    
    def test_operator_PLUS_should_apply_binary_action_upon_success(self):
        # accept when both match
        action    = lambda a,b: a.lower()+","+b.lower()
        parse_txt = text("GO") + "GO"
        parse_txt.action(action)
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(2, "go,go")))
        
    # Test combinator alt
    def test_combinator_alt_must_reject_when_token_matches_none_of_the_options(self):
        parse_txt = text("Hello").alt("Hi")
        result    = parse_txt(['Bonjour', 'tout', 'le', 'monde'])
        self.assertEqual(
            str(result),
            str(Failure(0, "Expected Hi instead of Bonjour")))
         
    def test_combinator_alt_should_accept_when_token_matches_first_alternative(self):
        parse_txt = text("GO").alt("BANG")
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'GO')))
        
    def test_combinator_alt_should_accept_when_token_matches_second_alternative(self):
        parse_txt = text("BANG").alt("GO")
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'GO')))
    
    def test_combinator_alt_should_accept_first_matching_alternative_when_both_branches_are_valid(self):
        left      = text("GO", action=lambda x: x.lower())
        right     = regex(r"\w+",action=lambda x: x.upper())
        parse_txt = left.alt(right)
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'go')))
         
    def test_combinator_alt_should_accept_parser_as_argument(self):
        parse_txt = text("blablabla").alt(regex(r"\w+"))
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'GO')))
     
    def test_combinator_alt_should_apply_unary_action_upon_success(self):
        action    = lambda x: x.lower()
        parse_txt = text("GO").alt("BANG", action=action)
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, "go")))
        
    # Test combinator |
    def test_operator_PIPE_must_reject_when_token_matches_none_of_the_options(self):
        parse_txt = text("Hello") | "Hi"
        result    = parse_txt(['Bonjour', 'tout', 'le', 'monde'])
        self.assertEqual(
            str(result),
            str(Failure(0, "Expected Hi instead of Bonjour")))
         
    def test_operator_PIPE_should_accept_when_token_matches_first_alternative(self):
        parse_txt = text("GO") | "BANG"
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'GO')))
        
    def test_operator_PIPE_should_accept_when_token_matches_second_alternative(self):
        parse_txt = text("BANG") | "GO"
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'GO')))
        
    def test_operator_PIPE_should_accept_first_matching_alternative_when_both_branches_are_valid(self):
        left      = text("GO", action=lambda x: x.lower())
        right     = regex(r"\w+",action=lambda x: x.upper())
        parse_txt = left | right
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'go')))
         
    def test_operator_PIPE_should_accept_parser_as_argument(self):
        parse_txt = text("blablabla") | regex(r"\w+")
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, 'GO')))
     
    def test_operator_PIPE_should_apply_unary_action_upon_success(self):
        action    = lambda x: x.lower()
        parse_txt = text("GO") | "BANG"
        parse_txt.action(action)
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, "go")))
        
    # Test change action
    def test_an_action_can_be_set_to_an_existing_parser(self):
        action    = lambda x: x.lower()
        parse_txt = text("GO")
        parse_txt.action(action)
        result    = parse_txt(['GO', 'GO', '!'])
        self.assertEqual(
            str(result),
            str(Success(1, "go")))

