## PAM Docker sandbox example

A worked example of the Docker sandbox. The submissions cover a
correct solution, a buggy one, an error-y one, and several malicious
ones (infinite loop, fork bomb, memory hog, disk hog, outbound
network, host-filesystem probes).

> The malicious submissions are only safe to run with `docker_enabled
> = True`. The bundled [config.py](./config.py) sets it.

### Layout

```
config.py               Docker-enabled UAM config
directories.txt         submission paths
dirs_and_names.txt      submission path,name pairs
groups.txt              group-name,dir-name,student-id
students.csv            classlist
test_solution.py        stdlib-only test driver (no pam.py needed)
submissions/<name>/A1/solution.py
```

The driver runs a fixed spec against the student's `solution.py` and
writes a UAM-compatible `result.json`. It uses only the Python stdlib
so the example works with a plain `python:3.11-slim` image — no
`testtools` install needed inside the (offline) container.

### Run

```sh
docker pull python:3.11-slim
python3 test_runner.py pam/docker_examples/config.py
```

Each `submissions/*/A1` should end up with a `result.json`. Aggregate
and template as usual:

```sh
python3 aggregator.py A1 \
    pam/docker_examples/dirs_and_names.txt \
    pam/docker_examples/students.csv \
    pam/docker_examples/groups.txt
python3 templator.py aggregated.json html
```

### What each submission proves

| Submission | What it exercises |
| --- | --- |
| `correct` / `failures` / `errors` | baseline pass/fail/error classification |
| `infloop` | `docker_timeout` (no `result.json`, container killed) |
| `forkbomb` | dropped capabilities + container PID namespace |
| `memhog` | `docker_memory` (OOM kill, no `result.json`) |
| `diskhog` | `docker_disk` via `--ulimit fsize` — write fails with EFBIG, recorded under `errors` |
| `network` | `docker_network = 'none'` — `OSError: Network is unreachable` |
| `host_escape` | bind-mount scope + `--cap-drop ALL` + `no-new-privileges` — probes fail silently |

If any row behaves differently, the sandbox is misconfigured. See the
[top-level README](../../README.md#docker-sandbox) for the storage
driver / bind mount caveats.
