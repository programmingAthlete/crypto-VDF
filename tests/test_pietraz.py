import unittest

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF


class TestPietrazVDF(unittest.TestCase):

    def test_setup(self):
        sec_param = 100
        delay = 4
        pp = PietrzakVDF.setup(security_param=sec_param, delay=delay)
        self.assertTrue(isinstance(pp, PublicParams))

    def test_compute_verify(self):
        x = 10
        modulus = 21

        pp = PublicParams(delay=2, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=4, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=6, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)

        self.assertTrue(verification)
        pp = PublicParams(delay=8, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=22, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=102, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=402, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)

        pp = PublicParams(delay=602, modulus=modulus)
        out = PietrzakVDF.sol(public_params=pp, input_param=x)
        proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=out)
        verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=proof)
        self.assertTrue(verification)
