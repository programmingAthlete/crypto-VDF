from abc import ABC, abstractmethod

from crypto_VDF.custom_errors.custom_exceptions import PrimeNumberNotFound
from crypto_VDF.data_transfer_objects.dto import PublicParams, RsaPrimes
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.utils.utils import square_sequences


class VDF(ABC):

    @classmethod
    @abstractmethod
    def setup(cls, security_param: int, delay: int) -> PublicParams:
        """
        Verifiable delay function setup function.

        Args:
            security_param: security parameter lambda
            delay: sequential parameter t
        Returns:
            public parameters pp
        """
        pass

    @classmethod
    @abstractmethod
    def verify(cls, public_params, input_param: int, output_param: int, proof=None):
        """
        Verify the output of the VDF

        Args:
            public_params: public parameters pp
            input_param: input to the VDF x
            output_param: output to the VDF y
            proof: proof pi of computation of the output (optional)
        Returns:
            True -> output/proof valid, False -> output/proof not valid
        """
        pass

    @classmethod
    def eval_function(cls, public_params, input_param):
        return square_sequences(steps=public_params.delay, a=input_param, n=public_params.modulus)

    @staticmethod
    def generate_rsa_primes(security_param) -> RsaPrimes:
        try:
            resp_q = PrimNumbers.k_bit_prim_number(security_param // 2, t=100000)
            resp_p = PrimNumbers.k_bit_prim_number(security_param // 2, t=100000)
        except PrimeNumberNotFound as exc:
            raise exc
        return RsaPrimes(p=resp_p, q=resp_q)
