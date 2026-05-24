"""UAM test driver for the PAM Docker sandbox example.

Staged into each student's directory by the config's preamble, then
run inside the container. Runs a fixed spec against ``solution.py``
(safe_sum + safe_average) and writes a UAM-compatible result.json.
Uses only the stdlib so no installs are needed inside the sandbox.
"""

import json
import os
import sys
import traceback


# The aggregate HTML template groups by test_id.split('.')[:2], so
# this string and every test ID must share the same prefix.
TEST_CASE = 'docker_examples.SolutionTests'


SPEC = [   # (method_name, callable taking the solution module, expected)
    ('test_sum_empty',     lambda s: s.safe_sum([]),          0),
    ('test_sum_one',       lambda s: s.safe_sum([42]),        42),
    ('test_sum_many',      lambda s: s.safe_sum([1, 2, 3, 4]), 10),
    ('test_sum_negatives', lambda s: s.safe_sum([-1, 1, -2, 2]), 0),
    ('test_avg_empty',     lambda s: s.safe_average([]),       0.0),
    ('test_avg_one',       lambda s: s.safe_average([10]),     10.0),
    ('test_avg_many',      lambda s: s.safe_average([2, 4, 6]), 4.0),
]


def _full_id(method):
    return '{}.{}'.format(TEST_CASE, method)


def _empty_result():
    return {
        'students': [],
        'results': {},
        'date': 'N/A',
        'assignment': 'N/A',
        'tests': [_full_id(method) for method, _, _ in SPEC],
    }


def _record(results, test_class, bucket, test_id, payload):
    results.setdefault(test_class, {}).setdefault(bucket, {})[test_id] = payload


def run():
    result = _empty_result()

    try:
        import solution  # noqa: E402 -- imported from cwd
    except Exception:
        # Importing the student file itself crashed (e.g. SyntaxError).
        # Record every spec entry as an error and bail out.
        details = traceback.format_exc()
        for method, _, _ in SPEC:
            test_id = _full_id(method)
            _record(result['results'], TEST_CASE, 'errors', test_id, {
                'description': 'Importing solution.py',
                'message': 'Could not import solution module.',
                'details': details,
            })
        return result

    for method, call, expected in SPEC:
        test_id = _full_id(method)
        try:
            actual = call(solution)
        except Exception as exc:
            _record(result['results'], TEST_CASE, 'errors', test_id, {
                'description': method,
                'message': '{}: {}'.format(type(exc).__name__, exc),
                'details': traceback.format_exc(),
            })
            continue

        if actual == expected:
            _record(result['results'], TEST_CASE, 'passes', test_id, method)
        else:
            _record(result['results'], TEST_CASE, 'failures', test_id, {
                'description': method,
                'message': 'expected {!r}, got {!r}'.format(expected, actual),
                'details': '',
            })

    return result


def main():
    target = os.environ.get('UAM_RESULT_JSON', 'result.json')
    payload = run()
    with open(target, 'w') as fp:
        json.dump(payload, fp, indent=2)
    # Exit non-zero if any test errored or failed, so the test runner
    # can flag the run as abnormal.
    for test in payload['results'].values():
        if test.get('errors') or test.get('failures'):
            sys.exit(1)


if __name__ == '__main__':
    main()
