from typing import List

from crypto_VDF.custom_errors.custom_exceptions import CoPrimeException
from crypto_VDF.data_transfer_objects.dto import RsaSetup, EvalResponse
from crypto_VDF.utils.logger import set_level, get_logger
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.utils.utils import hash_function, exp_non_modular, exp_modular, square_sequences, square_sequences_v2
from crypto_VDF.verifiable_delay_functions.vdf import VDF
from sympy import nextprime
import random

_log = get_logger(__name__)


class WesolowskiVDF(VDF):

    @classmethod
    def setup(cls, security_param: int, delay: int, ret_sk: bool = False) -> RsaSetup:
        primes = cls.generate_rsa_primes(security_param=security_param)
        p, q = primes.p.base_10, primes.q.base_10
        if ret_sk:
            return RsaSetup(n=p * q, phi=(p - 1) * (q - 1), security_param=security_param, delay=delay)
        else:
            return RsaSetup(n=p * q, security_param=security_param, delay=delay)

    @classmethod
    def trapdoor(cls, input_param: int, setup: RsaSetup) -> EvalResponse:
        exp = exp_non_modular(a=2, exponent=setup.delay) % setup.phi
        y = exp_modular(a=input_param, exponent=exp, n=setup.n)
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=y)
        r = y % prime_l
        q = ((y-r) // prime_l) % setup.phi
        proof = exp_modular(a=input_param, exponent=q, n=setup.n)
        return EvalResponse(output=y, proof=proof)

    @staticmethod
    def gen(setup: RsaSetup):
        numb = random.randint(2, setup.n)
        while NumberTheory.gcd(a=numb, b=setup.n) is False:
            numb = random.randint(2, setup.n)
        return numb

    @classmethod
    @set_level(logger=_log)
    def eval(cls, setup: RsaSetup, input_param, _verbose: bool = False) -> EvalResponse:
        y = square_sequences_v2(steps=setup.delay, a=input_param, n=setup.n)
        _log.info(f"[EVALUATION] VDF output: {y[0]}")
        if not NumberTheory.gcd(a=y[0], b=setup.n) == 1:
            raise CoPrimeException(message=f"Output y = {y} id not invertible in Z{setup.n}")
        proof = cls.compute_proof_opt(setup=setup, input_param=input_param, output_param=y[0], output_list=y[1])
        _log.info(f"[EVALUATION] VDF proof: {y}")
        return EvalResponse(output=y[0], proof=proof)

    @classmethod
    @set_level(logger=_log)
    def compute_proof(cls, setup: RsaSetup, input_param: int, delay: int, output_param: int,
                      _verbose: bool = False) -> int:
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=output_param)
        _log.debug(f"[COMPUTE-PROOF] Generated prime l from flat_shamir_hash: {prime_l}")
        exp = exp_non_modular(a=2, exponent=delay)
        return exp_modular(a=input_param, exponent=(exp // prime_l), n=setup.n)

    @staticmethod
    def alg_4(prime_l: int, delay: int):
        r = 1
        return [2 * (r := 2 * r % prime_l) // prime_l for _ in range(delay)]

    @staticmethod
    def compute_contribution(bit_val, output_list, idx, delay):
        if bit_val == 1:
            return output_list[delay - idx - 1]
        else:
            return 1

    @classmethod
    def compute_proof_opt(cls, setup: RsaSetup, input_param: int, output_param: int,
                          output_list: List[int]):
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=output_param)
        _log.debug(f"[COMPUTE-PROOF] Generated prime l from flat_shamir_hash: {prime_l}")
        bs = cls.alg_4(prime_l=prime_l, delay=setup.delay)
        proof = 1
        for i in range(len(output_list)):
            if bs[i] == 1:
                proof *= output_list[setup.delay - i - 1]
        return proof

    @classmethod
    @set_level(logger=_log)
    def verify(cls, setup: RsaSetup, input_param: int, output_param: int, proof: int, _verbose: bool = False):
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=output_param)
        _log.debug(f"[VERIFY] Generated prime l from flat_shamir_hash: {prime_l}")
        r = exp_modular(a=2, exponent=setup.delay, n=setup.n)
        _log.debug(f"[VERIFY] Value of r = 2^T % n: {r}")
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
