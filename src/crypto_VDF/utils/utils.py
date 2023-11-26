def square_sequences(a: int, steps: int, n: int) -> int:
    """
    Modular exponentiation

    Args:
        a: number to exponentiate
        steps: exponent
        n: modulus

    Returns:
        a^exponent (mod n)
    """
    c = abs((a * a) % n)
    for _ in range(steps):
        c *= abs((a * a) % n)
    return c


def exp_modular(a: int, exponent: int, n: int) -> int:
    """
    Modular exponentiation

    Args:
        a: number to exponentiate
        exponent: exponent
        n: modulus

    Returns:
        a^exponent (mod n)
    """
    exp = [int(item) for item in bin(exponent)[2:]]
    c = a
    for i in range(1, len(exp)):
        c = c * c % n
        if exp[i] == 1:
            c = c * a % n
    return c


def int_2_base(a: int, base: int) -> list:
    """
    Convert integer to base "base"

    Args:
        a: integer to convert to big number form in base "base"
        base:  base into which to convert integer "a"
    Returns:
        bin number form in base "base" corresponding to "a"
    """
    x = a
    reminders = []
    while x != 0:
        q = x // base
        r = x % base
        x = q
        reminders.append(r)
    return reminders[::-1]


def base_to_10(numb: [int], base: int) -> int:
    """
    Convert number from base "base" to base 10 integer

    :param numb: number in big number form in base "base" in [a_k,a_{k-1},..a_1,a_0] form
    :param base: base in which "numb" is written
    :return: integer corresponding to the base 10 of "numb"
    """
    base_10 = 0
    for i in range(len(numb)):
        base_10 += numb[::-1][i] * base ** i
    return base_10
