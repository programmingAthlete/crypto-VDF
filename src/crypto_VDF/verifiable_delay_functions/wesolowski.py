from crypto_VDF.custom_errors.custom_exceptions import CoPrimeException
from crypto_VDF.data_transfer_objects.dto import RsaSetup
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.utils.utils import hash_function, exp_non_modular, exp_modular, square_sequences
from crypto_VDF.verifiable_delay_functions.vdf import VDF
from sympy import nextprime
import random


class WesolowskiVDF(VDF):

    @classmethod
    def key_gen(cls, security_param: int, ret_sk: bool = False) -> RsaSetup:
        primes = cls.generate_rsa_primes(security_param=security_param)
        p, q = primes.p.base_10, primes.q.base_10
        if ret_sk:
            return RsaSetup(n=p * q, phi=(p - 1) * (q - 1), security_param=security_param)
        else:
            return RsaSetup(n=p * q, security_param=security_param)

    @classmethod
    def trapdoor(cls, input_param: int, setup: RsaSetup, delay: int):
        exp = exp_non_modular(a=2, exponent=delay) % setup.phi
        return exp_modular(a=input_param, exponent=exp, n=setup.n)

    @classmethod
    def setup(cls, security_param, delay):
        pass

    @staticmethod
    def gen(setup: RsaSetup):
        numb = random.randint(2, setup.n)
        while NumberTheory.gcd(a=numb, b=setup.n) is False:
            numb = random.randint(2, setup.n)
        return numb

    @classmethod
    def eval(cls, setup: RsaSetup, input_param, delay: int):
        y = square_sequences(steps=delay, a=input_param, n=setup.n)
        if not NumberTheory.gcd(a=y, b=setup.n) == 1:
            raise CoPrimeException(message=f"Output y = {y} id not invertible in Z{setup.n}")
        proof = cls.compute_proof(setup=setup, input_param=input_param, output_param=y, delay=delay)
        return y, proof

    @classmethod
    def compute_proof(cls, setup: RsaSetup, input_param: int, delay: int, output_param: int) -> int:
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=output_param)
        exp = exp_non_modular(a=2, exponent=delay)
        return exp_modular(a=input_param, exponent=(exp // prime_l), n=setup.n)

    @classmethod
    def verify(cls, setup: RsaSetup, input_param: int, output_param: int, proof=None, delay: int = None):
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=output_param)
        r = exp_modular(a=2, exponent=delay, n=setup.n)
        if exp_modular(a=proof, exponent=prime_l, n=setup.n) * exp_modular(a=input_param, exponent=r, n=setup.n):
            return True
        else:
            return False

    @staticmethod
    def flat_shamir_hash(security_param: int, g: int, y: int):
        params = f"{bin(g)[2:]}*{bin(y)[2:]}".encode()
        h = hash_function(hash_input=params, truncate_to=2 * security_param)
        if PrimNumbers.robin_miller_test(n=h) is True:
            return h
        else:
            return nextprime(h)
