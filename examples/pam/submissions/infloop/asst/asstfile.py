"""Sample student submission."""

import helper # importing student-written module
import math # importing standard module

def call_helper():
    return helper.func()

def call_math():
    return math.pi

def count_letter(s, c):
    """(str, str) -> int
    Given a string s and a character c, return the number of
    occurrences of c in s.
    >>> count_letter('anya', 'a')
    2
    >>> count_letter('anya', 'x')
    0
    """

    count = 0
    while True:        # inf loop
        count = 42
    return count

def remove_digits(s):
    """(str) -> str
    Return a string that is the same as s, but with digits removed.
    >>> remove_digits('csca20')
    'csca'
    >>> remove_digits('1cs3ca20')
    'csca'
    """

    new_s = ''
    for letter in s:
        if not letter.isdigit():
            new_s += letter
    return new_s

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
