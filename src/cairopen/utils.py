"""Utilities for Cairo felt conversions."""

import math


MAX_FELT = 2**251 + 17 * 2**192 + 1
MAX_UINT256 = (2**128 - 1, 2**128 - 1)
ZERO_ADDRESS = 0
TRUE = 1
FALSE = 0


#
# Felt manipulation
#


def ss_to_felt(text):
    """Converts a short string (<= 31 char) to a felt."""
    return int.from_bytes(bytes(text, "ascii"), "big")


def felt_to_ss(felt):
    """Converts a felt to a short string (<= 31 char)"""
    return felt.to_bytes(31, "big").decode()


def str_to_felt_arr(text):
    """Converts a string to a felt array."""
    return [ss_to_felt(c) for c in text]


def felt_arr_to_str(felt_arr):
    """Converts a felt array to a string."""
    chars = []
    for c in felt_arr:
        chars.append(c.to_bytes(1, "big").decode())
    return "".join(chars)


def uint(a):
    return (a, 0)


def to_uint(a):
    """Takes in value, returns uint256-ish tuple."""
    return (a & ((1 << 128) - 1), a >> 128)


def from_uint(uint):
    """Takes in uint256-ish tuple, returns value."""
    return uint[0] + (uint[1] << 128)


def add_uint(a, b):
    """Returns the sum of two uint256-ish tuples."""
    a = from_uint(a)
    b = from_uint(b)
    c = a + b
    return to_uint(c)


def sub_uint(a, b):
    """Returns the difference of two uint256-ish tuples."""
    a = from_uint(a)
    b = from_uint(b)
    c = a - b
    return to_uint(c)


def mul_uint(a, b):
    """Returns the product of two uint256-ish tuples."""
    a = from_uint(a)
    b = from_uint(b)
    c = a * b
    return to_uint(c)


def div_rem_uint(a, b):
    """Returns the quotient and remainder of two uint256-ish tuples."""
    a = from_uint(a)
    b = from_uint(b)
    c = math.trunc(a / b)
    m = a % b
    return (to_uint(c), to_uint(m))
