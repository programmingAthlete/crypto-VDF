import unittest
from unittest import skip

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF


class TestPietrazVDF(unittest.TestCase):

    def test_setup(self):
        sec_param = 100
        delay = 4
        pp = PietrzakVDF.setup(security_param=sec_param, delay=delay)
        self.assertTrue(isinstance(pp, PublicParams))

    def test_compute_verify_trivial_cases(self):
        x = 10
        modulus = 21

        # pp = PublicParams(delay=1, modulus=modulus, security_param=256)
        # y = PietrzakVDF.sol(public_params=pp, input_param=x)
        # out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # self.assertEqual(y, out)
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        # self.assertTrue(verification)
        pp = PublicParams(delay=2, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        self.assertTrue(y, out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        x = 11

        # pp = PublicParams(delay=1, modulus=modulus)
        # y = PietrzakVDF.sol(public_params=pp, input_param=x)
        # out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # self.assertEqual(y, out)
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        # self.assertTrue(verification)

        pp = PublicParams(delay=2, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        self.assertEqual(y, out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

    def test_compute_verify(self):
        x = 10
        modulus = 21

        pp = PublicParams(delay=2, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=4, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=8, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        # pp = PublicParams(delay=102, modulus=modulus)
        # out = PietrzakVDF.sol(public_params=pp, input_param=x)
        # proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        # self.assertTrue(verification)

        # pp = PublicParams(delay=402, modulus=modulus)
        # out = PietrzakVDF.sol(public_params=pp, input_param=x)
        # proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        # self.assertTrue(verification)

        # pp = PublicParams(delay=602, modulus=modulus)
        # out = PietrzakVDF.sol(public_params=pp, input_param=x)
        # proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        # self.assertTrue(verification)

        pp = PublicParams(delay=604, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

    @skip(reason='functionality sill not ready for delays not power of 2')
    def test_compute_verify_with_even_sub_numbers(self):
        # 10 and 11 are both such that x**2 % n in Zn*, however, 10 fails for odd delays verifications
        x = 11
        modulus = 21

        # pp = PublicParams(delay=10, modulus=modulus)
        # out = PietrzakVDF.sol(public_params=pp, input_param=x)
        # proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        # self.assertTrue(verification)

        pp = PublicParams(delay=50, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=10, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        x = 10
        pp = PublicParams(delay=10, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=50, modulus=modulus)
        y = PietrzakVDF.sol(public_params=pp, input_param=x)
        out, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)
