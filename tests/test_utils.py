import unittest

from crypto_VDF.utils import exp_modular


class TestUtils(unittest.TestCase):

    def test_exp_modular(self):
        res = exp_modular(2, 2, 10)
        self.assertEqual(res, 4)

        res = exp_modular(2, 2, 2)
        self.assertEqual(res, 0)

        res = exp_modular(10, 126, 29)
        self.assertEqual(res, 28)
