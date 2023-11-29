import random

from crypto_VDF.custom_errors.custom_exceptions import QuadraticResidueFailed


class NumberTheory:

    @staticmethod
    def gcd(a, b):
        """
        Euclidian algorithm to find the Greatest Common Divisor

        :param a:
        :param b:
        :return: gcd of a and b
        """
        r = a % b
        while r != 0:
            x = b
            b = r
            r = x % b
        return b

    @classmethod
    def check_quadratic_residue(cls, x, modulus):
        return cls.gcd(a=pow(abs(x), 2) % modulus, b=modulus) == 1

    @classmethod
    def generate_quadratic_residue(cls, modulus: int, max_iters=1000000000):
        i = 0
        while i < max_iters:
            x = random.randint(0, modulus - 1)
            if cls.check_quadratic_residue(x, modulus):
                return x
            i += 1
        raise QuadraticResidueFailed(
            f"Failed to create a quadratic residue of modulus {modulus} in {max_iters} iterations")
