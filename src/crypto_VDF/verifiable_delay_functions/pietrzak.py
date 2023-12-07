import logging
from typing import List

from crypto_VDF.custom_errors.custom_exceptions import PrimeNumberNotFound
from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.utils.utils import concat_hexs, flat_shamir_hash, exp_modular
from crypto_VDF.verifiable_delay_functions.vdf import VDF

logging.basicConfig(level=logging.INFO)

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


class PietrzakVDF(VDF):

    @classmethod
    def setup(cls, security_param, delay):
        try:
            resp_q = PrimNumbers.k_bit_prim_number(security_param // 2)
            resp_p = PrimNumbers.k_bit_prim_number(security_param // 2)
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
    def eval(cls, public_params, input_param):
        output = cls.eval_function(public_params=public_params, input_param=input_param)
        proof = cls.compute_proof(public_params=public_params, input_param=input_param, output_param=output)
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
            h_in = concat_hexs(x_i, int(2 ** t), y_i)
            _log.debug(f"[VERIFY] Hash input: {h_in}")
            r_i = flat_shamir_hash(x=h_in, y=item)
            _log.debug(f"[VERIFY] r_i = {r_i}")
            x_i = NumberTheory.modular_abs((exp_modular(a=x_i, exponent=r_i, n=public_params.modulus) * item) % public_params.modulus, public_params.modulus)
            y_i = NumberTheory.modular_abs((exp_modular(a=item, exponent=r_i, n=public_params.modulus) * y_i) % public_params.modulus, public_params.modulus)

            # x_i = (exp_modular(a=x_i, exponent=r_i, n=public_params.modulus) * item) % public_params.modulus
            # y_i = (exp_modular(a=item, exponent=r_i, n=public_params.modulus) * y_i) % public_params.modulus

            _log.debug(f"[VERIFY] x = {x_i} and y = {y_i}")
            _log.debug(
                f"[VERIFY] |xi| = {NumberTheory.modular_abs(x_i, public_params.modulus)},"
                f" |yi| = {NumberTheory.modular_abs(y_i, public_params.modulus)}\n")
            t = t / 2 if t % 2 == 0 else (t + 1) / 2
        _log.info(f"[VERIFY] x = {x_i} and y = {y_i}")
        _log.info(
            f"[VERIFY] |x| = {NumberTheory.modular_abs(x_i, public_params.modulus)}, "
            f"|y| = {NumberTheory.modular_abs(y_i, public_params.modulus)}")
        return y_i == NumberTheory.modular_abs(exp_modular(a=x_i, exponent=2, n=public_params.modulus),
                                               public_params.modulus)

    @staticmethod
    def compute_proof(public_params: PublicParams, input_param, output_param, log: bool = False) -> List[int]:
        if log is True:
            _log.setLevel(logging.DEBUG)
        x_i = input_param
        y_i = output_param
        _log.info(f"[COMPUTE-PROOF] Initial state: x = {x_i}, x**2 = {(x_i ** 2) % public_params.modulus}, y = {y_i}")
        mu = []
        i = 1
        t = public_params.delay
        while int(t) > 1:
            # Update t
            t_previous = t
            t = t / 2 if t % 2 == 0 else (t + 1) / 2
            _log.debug(f"[COMPUTE-PROOF] x = {x_i}, y={y_i}, exp = {int(2 ** t)}, t = {t}")
            # Calculate mi, hash and ri
            mu_i = exp_modular(a=x_i, n=public_params.modulus, exponent=int(2 ** t))
            assert NumberTheory.check_quadratic_residue(modulus=public_params.modulus, x=mu_i)
            _log.debug(f"[COMPUTE-PROOF] mu_i = {mu_i}")
            _log.debug(f"[COMPUTE-PROOF] 2 to t: {int(t_previous)}")
            h_in = concat_hexs(int(x_i), int(2 ** t_previous), int(y_i))
            _log.debug(f"[COMPUTE-PROOF] Hash input: {h_in}")
            r_i = flat_shamir_hash(x=h_in, y=int(mu_i))
            _log.debug(f"[COMPUTE-PROOF] r_i = {r_i}")

            # Update x_i any y_i
            x_i = NumberTheory.modular_abs(
                (exp_modular(a=x_i, exponent=r_i, n=public_params.modulus) * mu_i) % public_params.modulus,
                public_params.modulus)
            y_i = NumberTheory.modular_abs(
                (exp_modular(a=mu_i, exponent=r_i, n=public_params.modulus) * y_i) % public_params.modulus,
                public_params.modulus)
            _log.debug(f"[COMPUTE-PROOF] x = {x_i} and y = {y_i}")

            # Additional checks
            a = (x_i ** 2) % public_params.modulus
            _log.debug(f"[COMPUTE-PROOF] check: {a}")
            a = (y_i ** (int(2 ** t))) % public_params.modulus
            _log.debug(f"[COMPUTE-PROOF] check: {a}\n")
            mu.append(mu_i)
            i += 1
        _log.info(f"[COMPUTE-PROOF] Proof: {mu}")
        return mu


if __name__ == '__main__':
    pp = PietrzakVDF.setup(security_param=100, delay=8)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval_function(public_params=pp, input_param=x)
    print("Output of Eval:", y)
