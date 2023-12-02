import random

from crypto_VDF.custom_errors.custom_exceptions import QuadraticResidueFailed


class NumberTheory:

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Euclidian algorithm to find the Greatest Common Divisor

        Args:
            a:
            b:
        Returns:
            gcd of a and b
        """
        r = a % b
        while r != 0:
            x = b
            b = r
            r = x % b
        return b

    @classmethod
    def check_quadratic_residue(cls, x, modulus) -> bool:
        """
        Check if a number is a modular quadratic residue +

        Args:
            x: number to check if it is in QN_{modulus}^{+}
            modulus: modulo defining the group QN_{modulus}^{+}
        Returns:
            True if yes, False if no
        """
        return cls.gcd(a=pow(abs(x), 2) % modulus, b=modulus) == 1

    @classmethod
    def generate_quadratic_residue(cls, modulus: int, max_iters: int = 1000000000) -> int:
        """
        Generate a random number in QN_{modulus}^{+}

        Args:
            modulus:
            max_iters:
        Returns:
            Random number in QN_{modulus}^{+}
        Raises:
            Raises QuadraticResidueFailed if the number is not found
        """
        i = 0
        while i < max_iters:
            x = random.randint(0, modulus - 1)
            if cls.check_quadratic_residue(x, modulus):
                return x
            i += 1
        raise QuadraticResidueFailed(
            f"Failed to create a quadratic residue + of modulus {modulus} in {max_iters} iterations")

    @staticmethod
    def modular_abs(x, n):
        return min(x, n - x)
