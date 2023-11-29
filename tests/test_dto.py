import unittest

from pydantic import ValidationError

from crypto_VDF.custom_errors.custom_exceptions import ValuesDivergenceException
from crypto_VDF.data_transfer_objects.dto import KBitPrimeResponse


class TestDTOValidators(unittest.TestCase):

    def test_k_prime_bits_model(self):
        # Instantiate the model with empty base_2
        with self.assertRaises(ValidationError):
            KBitPrimeResponse(base_10=2, base_2=[])
        # Instantiate the model with wrong binary value
        with self.assertRaises(ValidationError):
            KBitPrimeResponse(base_10=2, base_2=[1, 1])
        # Correct instantiation
        model = KBitPrimeResponse(base_10=2, base_2=[1, 0])
        self.assertEqual(model.base_10, 2)
        self.assertEqual(model.base_2, [1, 0])
