from crypto_VDF.dto import PublicParams
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.verifiable_delay_functions.vdf import VDF


class PietrzakVDF(VDF):

    @classmethod
    def setup(cls, security_param, delay):
        resp_q = PrimNumbers.k_bit_prim_number(security_param // 2)
        resp_p = PrimNumbers.k_bit_prim_number(security_param // 2)
        if any(not item.status for item in [resp_p, resp_p]):
            raise Exception("Failed to generate random number")
        return PublicParams(modulus=resp_q.base_10 * resp_p.base_10, delay=delay)

    @classmethod
    def gen(cls, public_params):
        x = NumberTheory.generate_quadratic_residue(public_params.modulus)
        return x

    @classmethod
    def eval(cls, public_params, input_param):
        return cls.eval_function(public_params=public_params, input_param=input_param)

    @classmethod
    def verify(cls, public_params, input_param, output_param, proof=None):
        pass


if __name__ == '__main__':
    pp = PietrzakVDF.setup(security_param=100, delay=8)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval_function(public_params=pp, input_param=x)
    print("Output of Eval:", y)
