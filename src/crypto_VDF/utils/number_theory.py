import random

from crypto_VDF.custom_errors.custom_exceptions import QuadraticResidueFailed, CoPrimeException


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

    @classmethod
    def multiply(cls, u: int, v: int, n: int):
        x = (u * v) % n
        return NumberTheory.modular_abs(x, n)

    @classmethod
    def modular_inverse(cls, a: int, n: int) -> int:
        """
        Modular inverse of a in modulo n.
        Find u such that a * u + n * v = 1

        Args:
            a: integer of which to calculate the modular inverse
            n: modulus
        Returns:
            modular inverse of a in modulo n
        Raises:
            Raises CoPrimeException a and n are not co-primes
        """
        if cls.gcd(a, n) != 1:
            raise CoPrimeException(f"Integers {a} and {n} are not co-primes")
        r_list = [a, n]
        u = [1, 0]
        v = [0, 1]
        while r_list[-1] != 0:
            # Only store the latests two values of u,v and r's
            q = r_list[0] // r_list[1]
            u_value = u[0] - q * u[1]
            v_value = v[0] - q * v[1]
            u = [u[1], u_value]
            v = [v[1], v_value]
            r = r_list[0] % r_list[1]
            r_list = [r_list[1], r]
        return u[-2]
