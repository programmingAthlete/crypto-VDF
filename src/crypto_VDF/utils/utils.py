import os
import hashlib
from pathlib import Path
from typing import Tuple, List

from crypto_VDF.utils.number_theory import NumberTheory


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
    c = a % n
    for _ in range(steps):
        c = NumberTheory.modular_abs((c * c) % n, n)
    return c


def square_sequences_v2(a: int, steps: int, n: int) -> Tuple[int, List[int]]:
    """
    Modular exponentiation

    Args:
        a: number to exponentiate
        steps: exponent
        n: modulus

    Returns:
        a^exponent (mod n)
    """
    c = a % n
    cs = [c]
    for _ in range(steps):
        c = (c * c) % n
        cs.append(c)
    return c, cs


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
    if exponent == 0:
        return 1 % n
    exp = [int(item) for item in bin(exponent)[2:]]
    c = a
    for i in range(1, len(exp)):
        c = c * c % n
        if exp[i] == 1:
            c = c * a % n
    return c


def exp_non_modular(a: int, exponent: int) -> int:
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
        c = c * c
        if exp[i] == 1:
            c = c * a
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

    Args:
        numb: number in big number form in base "base" in [a_k,a_{k-1},..a_1,a_0] form
        base: base in which "numb" is written

    Returns:
        Integer corresponding to the base 10 of "numb"
    """
    base_10 = 0
    for i in range(len(numb)):
        base_10 += numb[::-1][i] * base ** i
    return base_10


def pad_zeros(func):
    def wrapper(x):
        f = func(x)
        if len(f) % 2 == 0:
            return f
        else:
            return '0' + f

    return wrapper


@pad_zeros
def get_hex(x):
    return '{:02x}'.format(x)


def concat_hexs(*args):
    hexs2 = [get_hex(item) for item in args]
    hex_string2 = ''.join(hexs2)
    return int(hex_string2, 16)


def hash_function(hash_input, truncate_to: int = None) -> int:
    if truncate_to is None or truncate_to > 256:
        truncate_to = 256
    h = hashlib.sha256(hash_input).hexdigest()[-truncate_to // 8 * 2]
    return int(h, 16)


def arrange_powers_of_2(start, stop) -> [int]:
    """
    creates a list of integers with values that are powers of two

    Args:
        start, stop: which number to start counting for powers of two and at which number to stop. (i.e range)
    Returns:
        List of Integers that are powers of two
    """
    result = []
    for i in range(start, stop + 1):
        result.append(2 ** i)

    return result


def get_current_file_abs_path(file):
    """
    create the absolute path for the file from which this function is called
    for example: if this function was called from /home/project/file.py it will
    return /home/project/file.py
    Args:
        file: the <<__file__>> global variable that each module (.py file) has.
    Returns:
        the absolute path to file from which this function was called
    """
    return os.path.realpath(file)


def create_path_to_data_folder(dataFolderName="data"):
    return os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        get_current_file_abs_path(__file__)
                    )
                )
            )
        )
        , dataFolderName)


def create_path_to_data_folder_v2(dataFolderName="data") -> Path:
    return Path(os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        get_current_file_abs_path(__file__)
                    )
                )
            )
        ), dataFolderName))
