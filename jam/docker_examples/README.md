## JAM Docker sandbox example

A worked example of the Docker sandbox for Java submissions. Mirrors
the [pam docker_examples](../../pam/docker_examples/README.md) but
for jam: correct, buggy, and a few malicious submissions (infinite
loop, memory hog, outbound network, host-filesystem probes).

> The malicious submissions are only safe to run with `docker_enabled
> = True`. The bundled [config.py](./config.py) sets it.

### Layout

```
config.py                       Docker-enabled UAM config
directories.txt                 submission paths
dirs_and_names.txt              submission path,name pairs
groups.txt                      group-name,dir-name,student-id
students.csv                    classlist
tests/TestSolution.java         JDK-only test driver (no JUnit / JAM jars)
submissions/<name>/A1/a1soln/Solution.java
```

The driver runs a fixed spec against the student's `a1soln.Solution`
and writes a UAM-compatible `result.json`. It uses only the JDK so the
example works with a plain `openjdk:11-slim` image.

### Run

```sh
docker pull openjdk:11-slim
python3 test_runner.py jam/docker_examples/config.py
```

Each `submissions/*/A1` should end up with a `result.json`. Aggregate
and template as usual:

```sh
python3 aggregator.py A1 \
    jam/docker_examples/dirs_and_names.txt \
    jam/docker_examples/students.csv \
    jam/docker_examples/groups.txt
python3 templator.py aggregated.json html
```

### What each submission proves

| Submission | What it exercises |
| --- | --- |
| `correct` / `failures` | baseline pass/fail classification |
| `infloop` | `docker_timeout` |
| `memhog` | `docker_memory` (JVM `OutOfMemoryError` or OOM kill) |
| `network` | `docker_network = 'none'` — `Socket.connect` fails |
| `host_escape` | bind-mount scope + dropped caps |
