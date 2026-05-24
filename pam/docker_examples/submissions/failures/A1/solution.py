"""Buggy solution: off-by-one in safe_sum, wrong empty-list contract in safe_average.

Exercises the 'failures' bucket of the test driver.
"""


def safe_sum(nums):
    total = 1  # off by one
    for n in nums:
        total += n
    return total


def safe_average(nums):
    # Spec says return 0.0 on empty; this raises instead -> recorded as
    # an error, not a failure. Wrong answer for non-empty input.
    return safe_sum(nums) / max(len(nums) - 1, 1)
