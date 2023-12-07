import unittest

from src.crypto_VDF.utils.prime_numbers import PrimNumbers


class TestPrimeNumbers(unittest.TestCase):

    def test_robin_miller_test(self):
        test_cases = [3, 5, 6, 7, 8, 11]
        for i in test_cases:
            x = PrimNumbers.robin_miller_test(i, 100)
            self.assertTrue(x) if i in [3, 5, 7, 11] else self.assertFalse(x)