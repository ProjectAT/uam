"""Allocates ~1 GiB. Only safe to run with docker_enabled = True.

bytearray(N) guarantees a fresh allocation per iteration; b'\\x00' * N
on its own would also allocate, but caching the chunk and reusing it
via `chunk * 1` would not (CPython returns the same object).
"""


def _eat_memory():
    chunks = []
    while len(chunks) <= 64:                        # 64 * 16 MiB = 1 GiB
        chunks.append(bytearray(16 * 1024 * 1024))
    return chunks


def safe_sum(nums):
    _eat_memory()
    return 0


def safe_average(nums):
    _eat_memory()
    return 0.0
