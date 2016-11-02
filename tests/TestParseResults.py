'''
This module contains the tests that validate the behavior of the various
possibilities of parse result

Author: X. Gillard
'''
import unittest

from pyparsers import ParseResult, Success, Failure

class TestParseResults(unittest.TestCase):
    
    def test_Sucess_are_equal_when_type_pos_and_value_are_equal(self):
        """
        This test validates that two `Success` objects are considered equal
        iff the two have the same type, value and the same position.
        """
        self.assertEqual(   Success(1, "Bonjour"), Success(1, "Bonjour"))
        self.assertNotEqual(Success(1, "Bonjour"), Success(2, "Bonjour"))
        self.assertNotEqual(Success(1, "Bonjour"), Success(1, "bonjour"))
        self.assertNotEqual(Success(1, "Bonjour"), Success(1, 42))
        self.assertNotEqual(Success(1, "Bonjour"), NotQuiteSuccess(1, "Bonjour", True))
    
    def test_Success_equal_is_reflexive(self):
        "Validates that `Success.__eq__` is implemented as a reflexive relation"
        result = Success(1, "Bonjour")
        self.assertEqual(result, result)
    
    def test_Success_equal_is_transtitive(self):
        "Validates that `Success.__eq__` is implemented as a transitive relation"
        result_1 = Success(1, "Bonjour")
        result_2 = Success(1, "Bonjour")
        result_3 = Success(1, "Bonjour")
        self.assertEqual(result_1, result_2)
        self.assertEqual(result_2, result_3)
        self.assertEqual(result_1, result_3)
    
    def test_Success_equal_is_symmetric(self):
        "Validates that `Success.__eq__` is implemented as a symmetric relation"
        result_1 = Success(1, "Bonjour")
        result_2 = Success(1, "Bonjour")
        self.assertEqual(result_1, result_2)
        self.assertEqual(result_2, result_1)
    
    def test_Success_equal_is_consistent_with_hash(self):
        "Validates that `Success.__eq__` is consistent with `Success.__hash__`"
        result_1 = Success(1, "Bonjour")
        result_2 = Success(1, "Bonjour")
        self.assertEqual(result_1, result_2)
        self.assertEqual(hash(result_2), hash(result_1))
    
    def test_Success_is_success(self):
        "The `success` method of a `Success` object should (by definition) yield True"
        self.assertTrue(Success(1, "True").success())
    
    def test_Success_has_no_reason(self):
        "The `reason` method of a `Success` object should (by definition) yield None"
        self.assertIsNone(Success(1, "True").reason())
    
    def test_Success_has_value(self):
        "A`Success` object should have a value"
        self.assertIsNotNone(Success(1, "True").value())
    
    def test_Success_none_is_an_acceptable_value(self):
        "A `Success` object should have a value but None is an acceptable value"
        self.assertIsNone(Success(1, None).value())
    
    def test_Success_transforms_yields_another_Success_with_transformed_value(self):
        """
        `Success.transform` must yield another `Success` object whose value is equivalent
        to the result of calling action with the success.value() as first argument.
        """
        initial = Success(1, "BONJOUR")
        expected= Success(1, "bonjour")
        action  = lambda x: x.lower()
        self.assertEqual(initial.transform(action), expected)
    
    def test_Success_string_representation(self):
        "Validates the implementation of the string representation of a `Success` object"
        self.assertEqual("Success(1, bonjour)", str(Success(1, "bonjour")))
    
    def test_Failure_are_equal_when_type_pos_and_reason_are_equal(self):
        """
        This test validates that two `Failure` objects are considered equal
        iff the two have the same type, reason and the same position.
        """
        self.assertEqual(   Failure(1, "Because"), Failure(1, "Because"))
        self.assertNotEqual(Failure(1, "Because"), Failure(2, "Because"))
        self.assertNotEqual(Failure(1, "Because"), Failure(1, "because"))
        self.assertNotEqual(Failure(1, "Because"), Failure(1, 42))
        self.assertNotEqual(Failure(1, "Because"), NotQuiteSuccess(1, "Because", False))
    
    def test_Failure_equal_is_reflexive(self):
        "Validates that `Failure.__eq__` is implemented as a reflexive relation"
        result = Failure(1, "Because !")
        self.assertEqual(result, result)
    
    def test_Failure_equal_is_transtitive(self):
        "Validates that `Failure.__eq__` is implemented as a transitive relation"
        result_1 = Failure(1, "Because")
        result_2 = Failure(1, "Because")
        result_3 = Failure(1, "Because")
        self.assertEqual(result_1, result_2)
        self.assertEqual(result_2, result_3)
        self.assertEqual(result_1, result_3)
    
    def test_Failure_equal_is_symmetric(self):
        "Validates that `Failure.__eq__` is implemented as a symmetric relation"
        result_1 = Failure(1, "Because")
        result_2 = Failure(1, "Because")
        self.assertEqual(result_1, result_2)
        self.assertEqual(result_2, result_1)
    
    def test_Failure_equal_is_consistent_with_hash(self):
        "Validates that `Failure.__eq__` is consistent with `Failure.__hash__`"
        result_1 = Failure(1, "Failure")
        result_2 = Failure(1, "Failure")
        self.assertEqual(result_1, result_2)
        self.assertEqual(hash(result_2), hash(result_1))
    
    def test_Failure_is_not_success(self):
        "The `success` method of a `Failure` object should (by definition) yield False"
        self.assertFalse(Failure(1, "True").success())
    
    def test_Failure_has_some_reason(self):
        "The `reason` method of a `Failure` object should provide an hint on the cause of the failure"
        self.assertEqual("Because", Failure(1, "Because").reason())
    
    def test_Failure_has_no_value(self):
        "The `success` method of a `Failure` object should (by definition) yield None"
        self.assertIsNone(Failure(1, "True").value())
    
    def test_Failure_transform_yields_self(self):
        "Validates that transform has no effect on a `Failure`"
        failure = Failure(1, "YOU ARE SCREWED !")
        action  = lambda x: x.lower()
        self.assertEqual(failure.transform(action), failure)
    
    def test_Failure_string_representation(self):
        "Validates the string representation of the `Failure` object"
        self.assertEqual("Failure(42, Because it is that way)", str(Failure(42, "Because it is that way")))
    
class NotQuiteSuccess(ParseResult):
    "A dummy test result"
    def __init__(self, p, v, s):
        self.p = p
        self.v = v
        self.s = s
    
    def value(self):
        return self.v
    
    def position(self):
        return self.p
    
    def success(self):
        return self.s