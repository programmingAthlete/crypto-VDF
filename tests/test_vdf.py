import unittest

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.vdf import VDF


class TestVDF(unittest.TestCase):

    def test_eval_function(self):
        pp = PublicParams(delay=4, modulus=3)
        res = VDF.eval_function(public_params=pp, input_param=2)
        self.assertEqual(res, 1)
