import unittest

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF


class TestPietrazVDF(unittest.TestCase):

    def test_setup(self):
        sec_param = 100
        delay = 4
        pp = PietrzakVDF.setup(security_param=sec_param, delay=delay)
        self.assertTrue(isinstance(pp, PublicParams))