## UAM

UAM stands for Universal AutoMarker. It is a framework for testing
student assignments written in a variety of programming languages,
collecting the results, and exporting them for easy viewing using
templates.

We currently provide full support for Python (pam) and Java (jam).

We are working on supporting SQL (sqam), Racket (ram), and Haskell
(ham).

We welcome collaboration and contributions!

## Requirements

You need Python >= 3.3 installed on your system. Then, install the
requirements listed in the file requirements.txt. The easiest way to
do this is to use pip (pip3 for Python 3):

`pip install -r /path_to_uam/requirements.txt`

You can use [virtualenv](https://virtualenv.pypa.io) to avoid
installing the packages system-wide.

To use JAM, you also need Java >= 7 installed in your system.

To use the Docker sandbox (see below), you also need Docker on your
PATH.

## Usage

The top level directory contains the framework scripts (test runner,
aggregator, and templator). The pam directory contains the Python
AutoMarker with instructions and examples, and the jam directory
contains the Java AutoMarker with instructions and examples.

See README files for [pam](./pam/README.md) and [jam](./jam/README.md)
for specific instructions.

## Docker sandbox

Student code is untrusted, so the test runner can wrap each `test_cmd`
in a disposable Docker container. To turn it on, add this to your
config:

```python
docker_enabled = True
docker_image   = 'python:3.11-slim'   # any image with your toolchain
docker_cpus    = '1.0'
docker_memory  = '256m'
docker_disk    = '1g'
docker_timeout = 60                   # seconds, enforced inside + outside
docker_network = 'none'               # 'bridge' if tests need it
```

Every setting has a default in [utils/defaults.py](./utils/defaults.py)
so you can leave any of them out. When Docker is enabled, the student's
directory is bind-mounted into the container (default `/submission`),
preamble/postamble still run on the host, and the container is removed
on exit.

A few notes worth knowing up front:

- The container runs as your host UID:GID by default (`docker_user =
  'host'`). This is required when `docker_drop_capabilities = True`
  (also the default) because `--cap-drop ALL` removes
  `CAP_DAC_OVERRIDE`, so container-root can't write to your bind
  mount.
- `docker_disk` emits both `--storage-opt size=` and
  `--ulimit fsize=`. The first only works on storage drivers with
  per-container quotas (XFS+pquota, btrfs, devicemapper, zfs); on
  ext4/overlayfs it's silently ignored. The ulimit half is enforced by
  the kernel and works everywhere, but only caps individual files —
  not total writes. For full coverage on a shared grading host, add a
  filesystem quota on the directory holding submissions.
- Anything `test_cmd` references must exist *inside* the image.
  Either bake your tools into a custom image or stage them into the
  student directory via `preamble_cmd` (which runs on the host, before
  the container starts).

## Support

Please send comments, feedback and bugs to
[anya@cs.utoronto.ca](mailto:anya@cs.utoronto.ca). Currently, there is
very limited support provided. We hope to improve.
