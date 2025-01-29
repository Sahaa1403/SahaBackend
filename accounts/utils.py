import secrets
import string
from random import randint


def random_N_chars_str(n: int) -> string:
    return (''.join(secrets.choice(string.ascii_uppercase + string.digits + string.digits) for _ in range(n)))


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)