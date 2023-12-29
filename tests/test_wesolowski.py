import unittest

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF


class TestWesolowski(unittest.TestCase):

    def test_flat_shamir_hash(self):
        pp = PublicParams(delay=10, modulus=21, security_param=10)
        g = 2
        y = 3

        r1 = WesolowskiVDF.flat_shamir_hash(g=g, y=y, security_param=10)
        self.assertTrue(PrimNumbers.robin_miller_test(n=r1))
        self.assertTrue(len(hex(r1)[2:]), pp.security_param // 8 * 2)

        r2 = WesolowskiVDF.flat_shamir_hash(g=g, y=y, security_param=10)
        self.assertTrue(PrimNumbers.robin_miller_test(n=r2))

        self.assertEqual(r1, r2)
