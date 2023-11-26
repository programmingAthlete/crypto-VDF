import random


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
        while True:
            x = random.randint(0, modulus - 1)
            if cls.check_quadratic_residue(x, modulus):
                break
            i += 1
        if not i == max_iters:
            return x
