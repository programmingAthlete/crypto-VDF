from typing import List, Tuple

from crypto_VDF.data_transfer_objects.dto import PublicParams, EvalResponse
from crypto_VDF.utils.logger import get_logger, set_level
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.utils import concat_hexs, hash_function, exp_modular, exp_non_modular, square_sequences, get_hex
from crypto_VDF.verifiable_delay_functions.vdf import VDF

_log = get_logger(__name__)


class PietrzakVDF(VDF):

    @classmethod
    def setup(cls, security_param: int, delay: int) -> PublicParams:
        primes = cls.generate_rsa_primes(security_param)
        return PublicParams(modulus=primes.q.base_10 * primes.p.base_10, delay=delay, security_param=security_param)

    @classmethod
    def gen(cls, public_params) -> int:
        return NumberTheory.generate_quadratic_residue(public_params.modulus)

    @classmethod
    def sol(cls, public_params, input_param) -> int:
        return cls.eval_function(public_params=public_params, input_param=input_param)

    @classmethod
    def eval(cls, public_params, input_param, _verbose: bool = False, _hide: bool = False) -> EvalResponse:
        output, proof = cls.compute_proof(public_params=public_params, input_param=input_param, _verbose=_verbose,
                                          _hide=_hide)
        return EvalResponse(output=output, proof=proof)

    @classmethod
    @set_level(logger=_log)
    def verify(cls, public_params, input_param, output_param, proof: List[int], _verbose: bool = False,
               _hide: bool = False) -> bool:
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
            exp = exp_non_modular(a=2, exponent=t)
            _log.debug(f"[VERIFY] x_i = {x_i}, y_i:{y_i}")
            r_i = cls.flat_shamir_hash(xi=x_i, exponent=exp, yi=y_i, mui=item, public_params=public_params)
            _log.debug(f"[VERIFY] r_i = {r_i}")
            x_i = NumberTheory.multiply(u=exp_modular(a=x_i, exponent=r_i, n=public_params.modulus), v=item,
                                        n=public_params.modulus)
            y_i = NumberTheory.multiply(u=exp_modular(a=item, exponent=r_i, n=public_params.modulus), v=y_i,
                                        n=public_params.modulus)
            _log.debug(f"[VERIFY] x = {x_i} and y = {y_i}\n")
            t = cls.calc_next_step(step=t)
        _log.info(f"[VERIFY] x = {x_i} and y = {y_i}\n")
        return y_i == NumberTheory.modular_abs(exp_modular(a=x_i, exponent=2, n=public_params.modulus),
                                               public_params.modulus)

    @staticmethod
    def calc_next_step(step: int) -> int:
        return step // 2 if step % 2 == 0 else (step + 1) // 2

    @staticmethod
    def flat_shamir_hash(public_params: PublicParams, xi, exponent, yi, mui) -> int:
        h_in = concat_hexs(int(xi), exponent, int(yi))
        hash_input = bytes.fromhex(get_hex(h_in)) + bytes.fromhex(get_hex(mui))
        return hash_function(hash_input=hash_input, truncate_to=public_params.security_param)

    @classmethod
    @set_level(logger=_log)
    def compute_proof(cls, public_params: PublicParams, input_param, _verbose: bool = False, _hide: bool = False) \
            -> Tuple[int, List[int]]:
        x_i = input_param
        t_half = cls.calc_next_step(step=public_params.delay)
        y_half = square_sequences(a=input_param, n=public_params.modulus, steps=t_half)
        y = square_sequences(a=y_half, n=public_params.modulus, steps=t_half)
        y_i = y
        _log.info(f"[COMPUTE-PROOF] Initial state: x = {x_i}, y = {y_i}")

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
                t = cls.calc_next_step(step=t)
                # Calculate mi, hash and ri
                mu_i = square_sequences(a=x_i, steps=t, n=public_params.modulus)
            exp_previous = exp_non_modular(a=2, exponent=t_previous)
            _log.debug(
                f"[COMPUTE-PROOF] x_i = {x_i}, y_i={y_i}, t = {t}, t_previous = {t_previous}")

            assert NumberTheory.check_quadratic_residue(modulus=public_params.modulus, x=mu_i)

            r_i = cls.flat_shamir_hash(xi=int(x_i), mui=int(mu_i), exponent=exp_previous, yi=y_i,
                                       public_params=public_params)
            _log.debug(f"[COMPUTE-PROOF] r_i = {r_i}")

            # Update x_i any y_i
            x_i = NumberTheory.multiply(u=exp_modular(a=x_i, exponent=r_i, n=public_params.modulus), v=mu_i,
                                        n=public_params.modulus)
            y_i = NumberTheory.multiply(u=exp_modular(a=mu_i, exponent=r_i, n=public_params.modulus), v=y_i,
                                        n=public_params.modulus)

            _log.debug(f"[COMPUTE-PROOF] x_i = {x_i} and y_i = {y_i}\n")
            mu.append(mu_i)
            i += 1
        _log.info(f"[COMPUTE-PROOF] Proof: {mu}")
        return y, mu


if __name__ == '__main__':
    pp = PietrzakVDF.setup(security_param=100, delay=8)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval_function(public_params=pp, input_param=x)
    print("Output of Eval:", y)
