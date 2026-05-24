"""UAM config for the PAM Docker sandbox example.

Several of the submissions under ``submissions/`` are hostile (infinite
loop, fork bomb, memory hog, disk hog, network probe, host escape), so
only run this with Docker enabled.

    docker pull python:3.11-slim
    python3 test_runner.py pam/docker_examples/config.py
"""

import os


max_processes = 4
timeout = 90   # host-side per-cmd timeout; must be >= docker_timeout


def timeout_operation():
    open('timedout', 'w').close()


students_fname = os.path.join('pam', 'docker_examples', 'directories.txt')

_EXAMPLES_DIR = os.path.dirname(os.path.abspath(__file__))
_TEST_DRIVER = os.path.join(_EXAMPLES_DIR, 'test_solution.py')

# Stage the test driver into each student's directory; the container
# then runs it from cwd (which is the bind-mounted /submission).
preamble_cmd = 'cp {} .'.format(_TEST_DRIVER)
test_cmd = ['python3 test_solution.py']
postamble_cmd = 'rm -rf test_solution.py __pycache__'


# Docker sandbox. Caps are set just above what `correct` needs and
# below what each malicious submission tries to consume.
docker_enabled = True
docker_image = 'python:3.11-slim'
docker_cpus = '1.0'
docker_memory = '256m'    # tripped by memhog
docker_disk = '1g'        # tripped by diskhog (via --ulimit fsize)
docker_timeout = 30       # tripped by infloop
docker_network = 'none'   # tripped by network
docker_drop_capabilities = True
docker_workdir = '/submission'


path_to_uam = os.path.abspath(os.path.join(_EXAMPLES_DIR, '..', '..'))
template_dir = os.path.join(path_to_uam, 'templates')
