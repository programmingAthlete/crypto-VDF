import hashlib
from functools import reduce
from typing import List

from crypto_VDF.custom_errors.custom_exceptions import CoPrimeException
from crypto_VDF.data_transfer_objects.dto import RsaSetup, EvalResponse
from crypto_VDF.utils.logger import set_level, get_logger
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.utils import hash_function, exp_non_modular, exp_modular, square_sequences_v2
from crypto_VDF.verifiable_delay_functions.vdf import VDF
from sympy import nextprime, isprime
import random

_log = get_logger(__name__)


class WesolowskiVDF(VDF):

    @staticmethod
    def alg_4_original(delay, prime_l, input_var, n):
        rs = []
        x = 1
        r = 1
        bs = []

        for _ in range(delay):
            b = (2 * r) // prime_l
            r = (2 * r) % prime_l
            bs.append(b)
            x = (exp_modular(a=x, exponent=2, n=n) * exp_modular(a=input_var, exponent=b, n=n)) % n

            rs.append(r)
        return x, bs, rs

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
        exp = exp_modular(a=2, exponent=setup.delay, n=setup.phi)
        y = exp_modular(a=input_param, exponent=exp, n=setup.n)
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=y)
        _log.info(f"[TRAPDOOR] Generated prime l: {prime_l}")
        r = exp % prime_l
        if (exp - r) % prime_l != 0:
            raise Exception("Invalid")
        q = ((exp - r) // prime_l) % setup.phi
        proof = exp_modular(a=input_param, exponent=q, n=setup.n)
        return EvalResponse(output=y, proof=proof)

    @staticmethod
    def hash_g(setup: RsaSetup, input_param: int):
        h = int(hashlib.sha3_256(f"residue{input_param}".encode()).hexdigest(), 16)
        out = h % setup.n
        if out in [1, -1]:
            raise Exception(f"g cannot be in {[-1, 1]}")
        return out

    @classmethod
    def gen(cls, setup: RsaSetup):
        numb = random.randint(2, setup.n)
        while True:
            try:
                return cls.hash_g(setup=setup, input_param=numb)
            except Exception as exc:
                _log.error(f"{exc}")
                continue

    @classmethod
    @set_level(logger=_log)
    def eval(cls, setup: RsaSetup, input_param, _verbose: bool = False, _hide: bool = False) -> EvalResponse:
        y = square_sequences_v2(steps=setup.delay, a=input_param, n=setup.n)
        _log.info(f"[EVALUATION] VDF output: {y[0]}")
        if not NumberTheory.gcd(a=y[0], b=setup.n) == 1:
            raise CoPrimeException(message=f"Output y = {y[0]} id not invertible in Z{setup.n}")
        proof = cls.compute_proof_opt(setup=setup, input_param=input_param, output_param=y[0], output_list=y[1])
        _log.info(f"[EVALUATION] VDF proof: {y[0]}")
        return EvalResponse(output=y[0], proof=proof)

    @classmethod
    @set_level(logger=_log)
    def eval_naive(cls, setup: RsaSetup, input_param, _verbose: bool = False) -> EvalResponse:
        y = square_sequences_v2(steps=setup.delay, a=input_param, n=setup.n)
        _log.info(f"[EVALUATION] VDF output: {y[0]}")
        if not NumberTheory.gcd(a=y[0], b=setup.n) == 1:
            raise CoPrimeException(message=f"Output y = {y[0]} is not invertible in Z{setup.n}")
        proof = cls.compute_proof_naive(setup=setup, input_param=input_param, output_param=y[0], delay=setup.delay)
        _log.info(f"[EVALUATION] VDF proof: {proof}")
        return EvalResponse(output=y[0], proof=proof)

    @classmethod
    @set_level(logger=_log)
    def compute_proof_naive(cls, setup: RsaSetup, input_param: int, delay: int, output_param: int,
                            _verbose: bool = False) -> int:
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=output_param)
        _log.debug(f"[COMPUTE-PROOF] Generated prime l from flat_shamir_hash: {prime_l}")
        exp = exp_non_modular(a=2, exponent=delay)
        return exp_modular(a=input_param, exponent=(exp // prime_l), n=setup.n)

    @staticmethod
    def get_component(idx: int, select_from: List[int], prime_l: int, delay):
        b = (2 * exp_modular(a=2, exponent=idx, n=prime_l)) // prime_l
        if b == 1:
            return select_from[delay - idx - 1]

    @classmethod
    def alg_4_revisited_comprehension(cls, n: int, prime_l: int, delay: int, output_list):
        _log.info("Starting Alg 4")
        proof_l = list(filter(lambda v: v is not None,
                              (cls.get_component(idx=i, select_from=output_list, prime_l=prime_l, delay=delay) for i in
                               range(delay))))
        if not proof_l:
            return 1
        proof = reduce(lambda x, y: (x * y) % n, proof_l)
        return proof

    @classmethod
    def alg_4_revisited(cls, n: int, prime_l: int, delay: int, output_list):
        _log.info("Starting Alg 4 revisited")
        r = 1
        proof_l = [1]
        for i in range(delay):
            b = (2 * r) // prime_l
            r = (2 * r) % prime_l
            if b == 1:
                proof_l.append(output_list[delay - i - 1])
        proof = reduce(lambda x, y: (x * y) % n, proof_l)
        return proof

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
        proof = cls.alg_4_revisited(n=setup.n, prime_l=prime_l, delay=setup.delay, output_list=output_list)
        return proof

    @classmethod
    @set_level(logger=_log)
    def verify(cls, setup: RsaSetup, input_param: int, output_param: int, proof: int, _verbose: bool = False,
               _hide: bool = False):
        prime_l = cls.flat_shamir_hash(security_param=setup.security_param, g=input_param, y=output_param)
        _log.debug(f"[VERIFY] Generated prime l from flat_shamir_hash: {prime_l}")
        r = exp_modular(a=2, exponent=setup.delay, n=prime_l)
        _log.debug(f"[VERIFY] Value of r = 2^T % n: {r}")
        if (exp_modular(a=proof, exponent=prime_l, n=setup.n) * exp_modular(a=input_param, exponent=r,
                                                                            n=setup.n)) % setup.n == output_param:
            return True
        else:
            return False

    @staticmethod
    def flat_shamir_hash(security_param: int, g: int, y: int):
        params = f"{bin(g)[2:]}*{bin(y)[2:]}".encode()
        h = hash_function(hash_input=params, truncate_to=2 * security_param)
        if isprime(h) is True:
            return h
        else:
            return nextprime(h)
