from abc import ABC, abstractmethod
from typing import Union, Tuple, List

from crypto_VDF.custom_errors.custom_exceptions import PrimeNumberNotFound
from crypto_VDF.data_transfer_objects.dto import PublicParams, RsaPrimes, RsaSetup, EvalResponse
from crypto_VDF.utils.prime_numbers import PrimNumbers
from crypto_VDF.utils.utils import square_sequences


class VDF(ABC):

    @classmethod
    @abstractmethod
    def setup(cls, security_param: int, delay: int):
        pass

    @classmethod
    @abstractmethod
    def eval(cls, setup: Union[PublicParams, RsaSetup], input_params: int, _verbose: bool = False) -> EvalResponse:
        """
        Eval Function

        Args:
            setup:
            input_params:
            _verbose:

        Returns:
            Output of the VDF and Proof
        """
        pass

    @classmethod
    @abstractmethod
    def verify(cls, setup: Union[PublicParams, RsaSetup], input_param: int, output_param: int,
               proof: Union[List[int], int]) -> bool:
        """
        Verify the output of the VDF

        Args:
            setup: public parameters pp
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
