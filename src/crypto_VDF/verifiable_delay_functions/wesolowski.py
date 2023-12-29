from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.utils.utils import hash_function
from crypto_VDF.verifiable_delay_functions.vdf import VDF
from sympy import nextprime


class WesolowskiVDF(VDF):

    @classmethod
    def setup(cls, security_param, delay):
        pass

    @classmethod
    def eval(cls, public_params, input_param):
        return cls.eval_function(public_params=public_params, input_param=input_param)

    @classmethod
    def verify(cls, public_params, input_param: int, output_param: int, proof=None):
        pass

    @staticmethod
    def flat_shamir_hash(public_params: PublicParams, g: int, y: int):
        params = f"{bin(g)[2:]}*{bin(y)[2:]}".encode()
        h = hash_function(hash_input=params, truncate_to=2 * public_params.security_param)
        if PrimNumbers.robin_miller_test(n=h) is True:
            return h
        else:
            nextprime(h)
