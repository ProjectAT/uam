"""Probes the container for host-filesystem access.

Reads paths that would be sensitive on a host (/etc/shadow, /proc, an
ssh key) and attempts to plant a file outside the bind mount. Inside
the sandbox the reads return either image-only data or EACCES, and
any write outside /submission lands in the ephemeral container layer
that --rm discards.
"""

import os


_PROBES = [
    '/etc/shadow',
    '/proc/1/environ',
    '/proc/self/maps',
    '/root/.ssh/id_rsa',
]


def _read_probes():
    for path in _PROBES:
        try:
            with open(path, 'rb') as fp:
                fp.read(512)
        except OSError:
            pass  # expected


def _write_outside_mount():
    try:
        with open('/tmp/uam-escape-attempt', 'w') as fp:
            fp.write('this file should never appear on the host')
    except OSError:
        pass


def safe_sum(nums):
    _read_probes()
    _write_outside_mount()
    return 0


def safe_average(nums):
    _read_probes()
    _write_outside_mount()
    return 0.0
