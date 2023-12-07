import unittest

from crypto_VDF.utils.number_theory import NumberTheory


class TestNumberTheory(unittest.TestCase):

    def test_check_quadratic_residue(self):
        a = NumberTheory.check_quadratic_residue(1, 2)
        self.assertTrue(a)

    def test_generate_random_quadratic_residue(self):
        x = NumberTheory.generate_quadratic_residue(1000000000)
        self.assertIsNotNone(x)

