import unittest

from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.utils import exp_modular, square_sequences, concat_hexs


class TestUtils(unittest.TestCase):

    def test_exp_modular(self):
        res = exp_modular(2, 2, 10)
        self.assertEqual(res, 4)

        res = exp_modular(2, 2, 2)
        self.assertEqual(res, 0)

        res = exp_modular(10, 126, 29)
        self.assertEqual(res, 28)

    def test_squaring_sequence(self):
        res = square_sequences(2, 4, 3)
        self.assertEqual(res, 1)
        res = square_sequences(10, 1, 21)
        self.assertEqual(res, NumberTheory.modular_abs(16, 21))

    def test_concat_hexs(self):
        x1 = 1
        x2 = 2
        res = concat_hexs(1, 2)
        h1, h2 = '{:02x}'.format(x1), '{:02x}'.format(x2)
        self.assertEqual(int(h1 + h2, 16), res)
