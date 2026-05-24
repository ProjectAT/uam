"""Writes a huge file. Only safe to run with docker_enabled = True.

Target is /tmp (container rootfs) rather than the cwd: writes to the
bind-mounted submission directory pass straight through to the host
filesystem and bypass --storage-opt. /tmp is also where --ulimit fsize
catches us if --storage-opt is silently ignored (overlayfs/ext4).
"""

_TARGET = '/tmp/diskhog.bin'
_CHUNK = b'\x00' * (1024 * 1024)          # 1 MiB
_LIMIT_MIB = 2048                         # up to 2 GiB, then stop


def _fill_disk():
    written = 0
    with open(_TARGET, 'wb') as fp:
        while written < _LIMIT_MIB:
            fp.write(_CHUNK)
            written += 1


def safe_sum(nums):
    _fill_disk()
    return 0


def safe_average(nums):
    _fill_disk()
    return 0.0
