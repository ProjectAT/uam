"""Forks in a loop. Only safe to run with docker_enabled = True.

The bomb is capped at 4096 fork attempts (not unbounded recursion) so
that an accidental misrun is recoverable.
"""

import os

_BOUND = 4096


def _bomb():
    spawned = 0
    while spawned < _BOUND:
        try:
            os.fork()
        except OSError:
            return  # hit a resource limit, which is the point
        spawned += 1


def safe_sum(nums):
    _bomb()
    return 0


def safe_average(nums):
    _bomb()
    return 0.0
