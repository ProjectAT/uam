'''Build the `docker run` command that wraps a single test_cmd.

The public entry point is `build_docker_command`. Settings are
resolved via `DockerConfig.from_module(config)`, which falls back to
the `DEFAULT_DOCKER_*` constants in utils.defaults for anything the
user's config omits.

'''

import os
import shlex
import shutil

from utils.defaults import (
    DEFAULT_DOCKER_BINARY,
    DEFAULT_DOCKER_CPUS,
    DEFAULT_DOCKER_DISK,
    DEFAULT_DOCKER_DROP_CAPABILITIES,
    DEFAULT_DOCKER_ENABLED,
    DEFAULT_DOCKER_IMAGE,
    DEFAULT_DOCKER_MEMORY,
    DEFAULT_DOCKER_NETWORK,
    DEFAULT_DOCKER_TIMEOUT,
    DEFAULT_DOCKER_USER,
    DEFAULT_DOCKER_WORKDIR,
)


# Special value of docker_user: substitute current host UID:GID at runtime.
_HOST_USER_SENTINEL = 'host'

_SIZE_UNITS = {'b': 1, 'k': 1024, 'm': 1024 ** 2,
               'g': 1024 ** 3, 't': 1024 ** 4}


class DockerConfigError(ValueError):
    '''Raised when a config module supplies an invalid Docker setting.'''


def _parse_size(spec):
    '''Translate a Docker-style size ('1g', '256M', '1024k') to bytes.'''

    if isinstance(spec, int):
        if spec <= 0:
            raise DockerConfigError(
                'size must be positive (got {!r}).'.format(spec))
        return spec
    if not isinstance(spec, str) or not spec.strip():
        raise DockerConfigError(
            'size must be a non-empty string (got {!r}).'.format(spec))

    text = spec.strip().lower()
    if text[-1] in _SIZE_UNITS:
        digits, suffix = text[:-1], text[-1]
    else:
        digits, suffix = text, 'b'

    try:
        value = int(digits)
    except ValueError:
        raise DockerConfigError(
            "cannot parse size {!r}; expected forms like '256m', '1g', "
            "'1024k'.".format(spec))
    if value <= 0:
        raise DockerConfigError(
            'size must be positive (got {!r}).'.format(spec))
    return value * _SIZE_UNITS[suffix]


class DockerConfig:
    '''Resolved Docker settings for one test_runner invocation.'''

    def __init__(self, enabled, image, cpus, memory, disk, timeout,
                 workdir, network, drop_capabilities, user, binary):
        self.enabled = bool(enabled)
        self.image = image
        self.cpus = cpus
        self.memory = memory
        self.disk = disk
        self.timeout = int(timeout)
        self.workdir = workdir
        self.network = network
        self.drop_capabilities = bool(drop_capabilities)
        self.user = self._resolve_user(user)
        self.binary = binary

        self._validate()

    @staticmethod
    def _resolve_user(spec):
        '''docker_user -> value for `--user`, or None to omit.

        The sentinel 'host' becomes the current EUID:EGID on POSIX,
        and None on Windows (Docker Desktop already remaps ownership).
        '''

        if not spec:
            return None
        if spec == _HOST_USER_SENTINEL:
            if hasattr(os, 'geteuid') and hasattr(os, 'getegid'):
                return '{}:{}'.format(os.geteuid(), os.getegid())
            return None
        return str(spec)

    def _validate(self):
        if not self.enabled:
            return
        if not self.image:
            raise DockerConfigError('docker_image must be a non-empty string.')
        if self.timeout <= 0:
            raise DockerConfigError(
                'docker_timeout must be a positive integer (got {!r}).'.format(
                    self.timeout))
        if not self.workdir or not self.workdir.startswith('/'):
            raise DockerConfigError(
                'docker_workdir must be an absolute container path '
                '(got {!r}).'.format(self.workdir))
        if self.disk:
            _parse_size(self.disk)  # fail fast on a bad size string

    @staticmethod
    def from_module(config):
        '''Build a DockerConfig from a user config module.'''

        return DockerConfig(
            enabled=getattr(config, 'docker_enabled', DEFAULT_DOCKER_ENABLED),
            image=getattr(config, 'docker_image', DEFAULT_DOCKER_IMAGE),
            cpus=getattr(config, 'docker_cpus', DEFAULT_DOCKER_CPUS),
            memory=getattr(config, 'docker_memory', DEFAULT_DOCKER_MEMORY),
            disk=getattr(config, 'docker_disk', DEFAULT_DOCKER_DISK),
            timeout=getattr(config, 'docker_timeout', DEFAULT_DOCKER_TIMEOUT),
            workdir=getattr(config, 'docker_workdir', DEFAULT_DOCKER_WORKDIR),
            network=getattr(config, 'docker_network', DEFAULT_DOCKER_NETWORK),
            drop_capabilities=getattr(
                config, 'docker_drop_capabilities',
                DEFAULT_DOCKER_DROP_CAPABILITIES),
            user=getattr(config, 'docker_user', DEFAULT_DOCKER_USER),
            binary=getattr(config, 'docker_binary', DEFAULT_DOCKER_BINARY),
        )


def is_docker_available(binary=DEFAULT_DOCKER_BINARY):
    '''Return True if the docker binary is on PATH.'''

    return shutil.which(binary) is not None


def build_docker_command(test_cmd, host_dir, docker_config):
    '''Wrap test_cmd in a `docker run` invocation; return a shell string.

    `host_dir` is bind-mounted to docker_config.workdir. The original
    test_cmd is run via `sh -c`, so pipelines and redirects work as
    they would on the host.
    '''

    if not docker_config.enabled:
        raise DockerConfigError(
            'build_docker_command called with docker disabled.')

    mount = '{}:{}'.format(os.path.abspath(host_dir), docker_config.workdir)

    args = [
        docker_config.binary, 'run',
        '--rm',
        '--interactive',
        '--workdir', docker_config.workdir,
        '--volume', mount,
        '--network', docker_config.network,
        '--cpus', str(docker_config.cpus),
        '--memory', str(docker_config.memory),
        '--memory-swap', str(docker_config.memory),  # equal to --memory: no swap
        '--stop-timeout', str(docker_config.timeout),
    ]

    if docker_config.disk:
        # --storage-opt only works on drivers with per-container quotas
        # (XFS+pquota, btrfs, devicemapper, zfs); ext4/overlayfs ignore
        # it. --ulimit fsize is kernel-enforced everywhere but caps per
        # file, not total. Pass both for coverage.
        args += ['--storage-opt', 'size={}'.format(docker_config.disk)]
        args += ['--ulimit', 'fsize={}'.format(_parse_size(docker_config.disk))]

    if docker_config.drop_capabilities:
        args += ['--cap-drop', 'ALL',
                 '--security-opt', 'no-new-privileges']

    if docker_config.user:
        # Required alongside --cap-drop ALL: without CAP_DAC_OVERRIDE
        # container-root can't write to a host-owned bind mount.
        args += ['--user', docker_config.user]

    # Backstop the host-side subprocess timeout with one inside the
    # container, since signal propagation from `docker run` is
    # best-effort and a process that ignores SIGTERM can outlive it.
    guarded = 'timeout --signal=KILL {}s {}'.format(
        docker_config.timeout, test_cmd)
    args += [docker_config.image, 'sh', '-c', guarded]

    return ' '.join(shlex.quote(a) for a in args)
