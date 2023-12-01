from random import randint
from typing import Generator

from crypto_VDF.custom_errors.custom_exceptions import PrimeNumberNotFound
from crypto_VDF.data_transfer_objects.dto import KBitPrimeResponse
from crypto_VDF.utils.utils import exp_modular, base_to_10


class PrimNumbers:

    @staticmethod
    def k_bit_numer(k: int) -> Generator[int, None, None]:
        """
        Generate an iterator object of k bits with the first bit being 1 (starting with the first bit being 0 is like
         having a k-1 bit number) and other k-1 random bits.

        Args:
            k: length of the iterator to return
        """
        if k > 1:
            yield 1
        for _ in range(k - 1):
            yield randint(0, 1)

    @staticmethod
    def fermat_test(n: int, t=100) -> bool:
        """
        Fermat Test - test if a number is prime

        :param t: repeat parameter of the Fermat Test
        :param n: numbers to test
        :return: True if n is prime and False if it isn't prime
        """
        for _ in range(t):
            a = randint(2, n - 2)
            r = exp_modular(a, n - 1, n)
            if r != 1:
                return False
        return True

    @classmethod
    def k_bit_prim_number(cls, k, t: int = 100, max_iter: int = 10000) -> KBitPrimeResponse:
        """
        Generate a k-bit prime number

        Args:
            k: length of bit of the prime number to generate
            t: repeat parameter of the Fermat Test
            max_iter: maximum possible iterations allowed for succeeding to generate the prime number -
            default max_iter = 10000 to have a high probability of successfully generating the prime number
             for k <= 2000 bits
        Returns:
            KBitPrimeResponse(status: bool, base_10: int, base_2: list)
        Raises:
            Raises PrimeNumberNotFound if the k-bt prime number is not fond
        """
        i = 0
        while i < max_iter:
            k_bit_n = list(cls.k_bit_numer(k))
            base_10_n = base_to_10(k_bit_n, 2)
            response = cls.fermat_test(n=base_10_n, t=t)
            if response:
                return KBitPrimeResponse(base_10=base_10_n, base_2=k_bit_n)
            i += 1
        raise PrimeNumberNotFound
