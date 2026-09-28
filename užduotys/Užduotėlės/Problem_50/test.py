# Problem: Buggy: Find the Maximum
# Difficulty: 3
# Topic: Debugging
#
# This function is SUPPOSED to find the largest number in a list
# (returning None for an empty list), but someone introduced a bug.
# Find it and fix it.
#
# Example:
#     numbers = [-5, -1, -3]  ->  -1
#
# Notes:
#     Test it on a list of all-negative numbers -- that's when this kind of
#     bug tends to show up.

def run(numbers):
    if len(numbers) == 0:
        return None
    biggest = 0
    for n in numbers:
        if n > biggest:
            biggest = n
    return biggest
