"""Solution that raises uncaught exceptions on most inputs.

Exercises the 'errors' bucket of the test driver.
"""


def safe_sum(nums):
    if not nums:
        raise ValueError('safe_sum got an empty list')
    return sum(nums) + nums[1234]  # IndexError on most non-empty inputs


def safe_average(nums):
    return sum(nums) / 0  # ZeroDivisionError, always
