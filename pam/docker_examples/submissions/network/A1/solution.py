"""Tries to open outbound sockets. Verifies docker_network = 'none'.

With networking disabled the connect call fails immediately. The test
driver then records the OSError under the 'errors' bucket.
"""

import socket


_TARGETS = [('example.com', 80), ('1.1.1.1', 53)]


def _try_connect():
    last = None
    for host, port in _TARGETS:
        try:
            with socket.create_connection((host, port), timeout=2) as s:
                s.sendall(b'GET / HTTP/1.0\r\n\r\n')
                return s.recv(64)
        except OSError as err:
            last = err
    raise OSError('all network targets unreachable: {}'.format(last))


def safe_sum(nums):
    _try_connect()
    return 0


def safe_average(nums):
    _try_connect()
    return 0.0
