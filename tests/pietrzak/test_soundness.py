import unittest

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF


class TestPietrazSoundness(unittest.TestCase):

    def test_fake_proof_verification(self):
        modulus = 21
        x = 10
        pp = PublicParams(delay=604, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        fake_proof = [1 for _ in proof]
        # Run the verification with a fake proof
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=fake_proof)
        # Check that the verification returns False
        self.assertFalse(verification)

        # Add test cases here

    def test_fake_output(self):
        modulus = 21
        x = 10

        pp = PublicParams(delay=604, modulus=modulus)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # Run the verification with a fake proof
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=11, proof=proof)
        # Check that the verification returns False
        self.assertFalse(verification)

        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=1000, proof=proof)
        self.assertFalse(verification)

        # Add test cases here

