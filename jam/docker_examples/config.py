"""UAM config for the JAM Docker sandbox example.

Several of the submissions under ``submissions/`` are hostile, so
only run this with Docker enabled.

    docker pull openjdk:11-slim
    python3 test_runner.py jam/docker_examples/config.py

The test driver under tests/TestSolution.java uses only the JDK, so
no JUnit / JAM jars are needed inside the container.
"""

import os


max_processes = 4
timeout = 120   # host-side per-cmd timeout; must be >= docker_timeout


def timeout_operation():
    open('timedout', 'w').close()


students_fname = os.path.join('jam', 'docker_examples', 'directories.txt')

_EXAMPLES_DIR = os.path.dirname(os.path.abspath(__file__))
_TEST_DRIVER = os.path.join(_EXAMPLES_DIR, 'tests', 'TestSolution.java')

# Stage the test driver, then compile + run inside the container.
preamble_cmd = 'cp {} .'.format(_TEST_DRIVER)
test_cmd = [
    'javac a1soln/Solution.java TestSolution.java && '
    'java -cp . TestSolution'
]
# `TestSolution$*.class` covers the inner-class files javac emits.
postamble_cmd = (
    "rm -f TestSolution.java && "
    "find . -maxdepth 2 -name '*.class' -delete"
)


# Docker sandbox. JVM needs more memory/disk than CPython.
docker_enabled = True
docker_image = 'openjdk:11-slim'
docker_cpus = '1.0'
docker_memory = '512m'
docker_disk = '2g'
docker_timeout = 60
docker_network = 'none'
docker_drop_capabilities = True
docker_workdir = '/submission'


uam_dir = os.path.abspath(os.path.join(_EXAMPLES_DIR, '..', '..'))
template_dir = os.path.join(uam_dir, 'templates')
