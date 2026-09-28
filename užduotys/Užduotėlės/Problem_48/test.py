# Problem: Buggy: List Average
# Difficulty: 3
# Topic: Debugging
#
# This function is SUPPOSED to return the average of a list of numbers,
# but someone introduced a bug. Find it and fix it.
#
# Example:
#     numbers = [1, 2, 3, 4]  ->  2.5

def run(numbers):
    if len(numbers) == 0:
        return None
    total = 0
    for n in numbers:
        total += n
    return total / (len(numbers) + 1)
