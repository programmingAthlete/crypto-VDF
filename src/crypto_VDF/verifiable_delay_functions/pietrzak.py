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
            _log.error("Not Quadratic residues")
            return False
        x_i = input_param
        y_i = output_param
        if len(proof) == 0:
            return y_i == (x_i ** 2) % public_params.modulus
        for i in range(len(proof)):
            print()
            t = public_params.delay / (2 ** i)
            _log.debug(f"2 to t: {2 ** t}")
            h_in = concat_hexs(x_i, int(2 ** t), y_i)
            _log.debug(f"Hash input: {h_in}")
            r_i = flat_shamir_hash(x=h_in, y=proof[i])
            _log.debug(f"r_i = {r_i}")
            x_i = (exp_modular(a=x_i, exponent=r_i, n=public_params.modulus) * proof[i]) % public_params.modulus
            y_i = (exp_modular(a=proof[i], exponent=r_i, n=public_params.modulus) * y_i) % public_params.modulus
            _log.debug(f"x = {x_i} and y = {y_i}")
            _log.debug(
                f"|xi| = {NumberTheory.modular_abs(x_i, public_params.modulus)},"
                f" |yi| = {NumberTheory.modular_abs(y_i, public_params.modulus)},")
        print()
        _log.info(f"x = {x_i} and y = {y_i}")
        _log.info(
            f"|x| = {NumberTheory.modular_abs(x_i, public_params.modulus)}, "
            f"|y| = {NumberTheory.modular_abs(y_i, public_params.modulus)}")
        return y_i == exp_modular(a=x_i, exponent=2, n=public_params.modulus)

    @staticmethod
    def compute_proof(public_params: PublicParams, input_param, output_param, log: bool = False) -> List[int]:
        if log is True:
            _log.setLevel(logging.DEBUG)
        x_i = input_param
        y_i = output_param
        _log.info(f"Initial: {(x_i ** 2) % public_params.modulus}")
        mu = []
        i = 1
        t = public_params.delay
        while int(t) > 1:
            print()
            t = public_params.delay / (2 ** i)
            exp = int(2 ** t)
            _log.debug(f"x = {x_i}, y={y_i}, exp = {exp}, t = {t}")
            mu_i = exp_modular(a=x_i, n=public_params.modulus, exponent=exp)
            assert NumberTheory.check_quadratic_residue(modulus=public_params.modulus, x=mu_i)
            _log.debug(f"mu_i = {mu_i}")

            t_step = public_params.delay / (int(2 ** (i - 1)))
            _log.debug(f"2 to t: {int(t_step)}")
            h_in = concat_hexs(int(x_i), int(2 ** t_step), int(y_i))
            _log.debug(f"Hash input: {h_in}")
            r_i = flat_shamir_hash(x=h_in, y=int(mu_i))
            _log.debug(f"r_i = {r_i}")

            # Update x_i any y_i
            x_i = (exp_modular(a=x_i, exponent=r_i, n=public_params.modulus) * mu_i) % public_params.modulus
            y_i = (exp_modular(a=mu_i, exponent=r_i, n=public_params.modulus) * y_i) % public_params.modulus
            _log.debug(f"x = {x_i} and y = {y_i}")
            a = (x_i ** 2) % public_params.modulus
            _log.debug(f"check: {a}")
            a = (y_i ** (int(2 ** t))) % public_params.modulus
            _log.debug(f"check: {a}")
            mu.append(mu_i)
            i += 1
        return mu


if __name__ == '__main__':
    pp = PietrzakVDF.setup(security_param=100, delay=8)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval_function(public_params=pp, input_param=x)
    print("Output of Eval:", y)
