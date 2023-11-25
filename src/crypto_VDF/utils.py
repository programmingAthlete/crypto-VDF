def exp_modular(a: int, exponent: int, n: int) -> int:
    """
    Modular exponentiation

    :param a: number to exponentiate
    :param exponent: exponent
    :param n: modulus
    :return: a^exponent (mod n)
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

    :param a: integer to convert to big number form in base "base"
    :param base: base into which to convert integer "a"
    :return: bin number form in base "base" corresponding to "a"
    """
    x = a
    reminders = []
    while x != 0:
        q = x // base
        r = x % base
        x = q
        reminders.append(r)
    return reminders[::-1]
