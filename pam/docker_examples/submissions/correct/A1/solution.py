"""Reference solution: passes all tests."""


def safe_sum(nums):
    total = 0
    for n in nums:
        total += n
    return total


def safe_average(nums):
    if not nums:
        return 0.0
    return safe_sum(nums) / len(nums)
