import logging
from typing import List

from crypto_VDF.custom_errors.custom_exceptions import PrimeNumberNotFound
from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.utils.logger import get_logger
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.utils.utils import concat_hexs, flat_shamir_hash, exp_modular, exp_non_modular, square_sequences
from crypto_VDF.verifiable_delay_functions.vdf import VDF

_log = get_logger(__name__)


class PietrzakVDF(VDF):

    @classmethod
    def setup(cls, security_param, delay):
        try:
            resp_q = PrimNumbers.k_bit_prim_number(security_param // 2, t=100000)
            resp_p = PrimNumbers.k_bit_prim_number(security_param // 2, t=100000)
            _log.info(f"[SETUP] Prime numbers p = {resp_p.base_10}, q = {resp_q.base_10}")
        except PrimeNumberNotFound as exc:
            raise exc
        return PublicParams(modulus=resp_q.base_10 * resp_p.base_10, delay=delay)

    @classmethod
    def gen(cls, public_params):
        return NumberTheory.generate_quadratic_residue(public_params.modulus)

    @classmethod
    def sol(cls, public_params, input_param):
        return cls.eval_function(public_params=public_params, input_param=input_param)

    @classmethod
    def compute_output(cls, public_params, input_param, delay):
        return square_sequences(steps=delay, a=input_param, n=public_params.modulus)

    @classmethod
    def eval(cls, public_params, input_param, verbose: int = False):
        output = cls.eval_function(public_params=public_params, input_param=input_param)
        proof = cls.compute_proof(public_params=public_params, input_param=input_param, log=verbose)
        return output, proof

    @classmethod
    def verify(cls, public_params, input_param, output_param, proof=None, log: bool = False) -> bool:
        if log is True:
            _log.setLevel(logging.DEBUG)
        if any(NumberTheory.check_quadratic_residue(modulus=public_params.modulus, x=item) is False for item in
               [input_param, output_param]):
            _log.error("[VERIFY] Not Quadratic residues")
            return False
        x_i = input_param
        y_i = output_param
        if len(proof) == 0:
            return y_i == NumberTheory.modular_abs((x_i ** 2) % public_params.modulus, public_params.modulus)
        t = public_params.delay
        for item in proof:
            _log.debug(f"[VERIFY] 2 to t: {2 ** t}, t = {t}")
            exp = exp_non_modular(a=2, exponent=t)
            h_in = concat_hexs(x_i, exp, y_i)
            _log.debug(f"[VERIFY] Hash input: {h_in}")
            r_i = flat_shamir_hash(x=h_in, y=item)
            _log.debug(f"[VERIFY] r_i = {r_i}")
            x_i = NumberTheory.modular_abs(
                (exp_modular(a=x_i, exponent=r_i, n=public_params.modulus) * item) % public_params.modulus,
                public_params.modulus)
            y_i = NumberTheory.modular_abs(
                (exp_modular(a=item, exponent=r_i, n=public_params.modulus) * y_i) % public_params.modulus,
                public_params.modulus)

            # x_i = (exp_modular(a=x_i, exponent=r_i, n=public_params.modulus) * item) % public_params.modulus
            # y_i = (exp_modular(a=item, exponent=r_i, n=public_params.modulus) * y_i) % public_params.modulus

            _log.debug(f"[VERIFY] x = {x_i} and y = {y_i}")
            _log.debug(
                f"[VERIFY] |xi| = {NumberTheory.modular_abs(x_i, public_params.modulus)},"
                f" |yi| = {NumberTheory.modular_abs(y_i, public_params.modulus)}\n")
            t = cls.calc_next_step(step=t)
        _log.info(f"[VERIFY] x = {x_i} and y = {y_i}")
        _log.info(
            f"[VERIFY] |x| = {NumberTheory.modular_abs(x_i, public_params.modulus)}, "
            f"|y| = {NumberTheory.modular_abs(y_i, public_params.modulus)}")
        return y_i == NumberTheory.modular_abs(exp_modular(a=x_i, exponent=2, n=public_params.modulus),
                                               public_params.modulus)

    @staticmethod
    def calc_next_step(step: int):
        return step // 2 if step % 2 == 0 else (step + 1) // 2

    @classmethod
    def compute_proof(cls, public_params: PublicParams, input_param, log: bool = False) -> List[int]:
        if log is True:
            _log.setLevel(logging.DEBUG)
        x_i = input_param
        t_half = cls.calc_next_step(step=public_params.delay)
        y_half = square_sequences(a=input_param, n=public_params.modulus, steps=t_half)
        y = square_sequences(a=y_half, n=public_params.modulus, steps=t_half)
        y_i = y
        _log.info(f"[COMPUTE-PROOF] Initial state: x = {x_i}, x**2 = {(x_i ** 2) % public_params.modulus},y = {y_i}")

        mu = []
        i = 1
        t = public_params.delay
        while int(t) > 1:
            if i == 1:
                mu_i = y_half
                t = t_half
                t_previous = public_params.delay
            else:
                t_previous = t
                # Update t
                # t_previous = public_params.delay // (2 ** (i - 1)) if t % 2 == 0 else (public_params.delay + 1) // (
                #       2 ** (i - 1))
                # t = public_params.delay // (2 ** i) if t % 2 == 0 else (public_params.delay + 1) // (2 ** i)
                t = cls.calc_next_step(step=t)
                # Calculate mi, hash and ri
                mu_i = square_sequences(a=x_i, steps=t, n=public_params.modulus)
            exp_previous = exp_non_modular(a=2, exponent=t_previous)
            _log.debug(
                f"[COMPUTE-PROOF] x = {x_i}, y={y_i}, t = {t}, t_previous = {t_previous},"
                f" exp_previous = {exp_previous}")

            # mu_i = exp_modular(a=x_i, n=public_params.modulus, exponent=exp)
            assert NumberTheory.check_quadratic_residue(modulus=public_params.modulus, x=mu_i)
            h_in = concat_hexs(int(x_i), exp_previous, int(y_i))
            _log.debug(f"[COMPUTE-PROOF] mu_i = {mu_i},  2 to t: {int(t_previous)}, Hash input: {h_in}")

            r_i = flat_shamir_hash(x=h_in, y=int(mu_i))
            _log.debug(f"[COMPUTE-PROOF] r_i = {r_i}")

            # Update x_i any y_i
            x_i = NumberTheory.multiply(u=exp_modular(a=x_i, exponent=r_i, n=public_params.modulus), v=mu_i,
                                        n=public_params.modulus)
            y_i = NumberTheory.multiply(u=exp_modular(a=mu_i, exponent=r_i, n=public_params.modulus), v=y_i,
                                        n=public_params.modulus)

            _log.debug(f"[COMPUTE-PROOF] x = {x_i} and y = {y_i}")
            mu.append(mu_i)
            i += 1
        _log.info(f"[COMPUTE-PROOF] Proof: {mu}")
        return mu


if __name__ == '__main__':
    pp = PietrzakVDF.setup(security_param=100, delay=8)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval_function(public_params=pp, input_param=x)
    print("Output of Eval:", y)
