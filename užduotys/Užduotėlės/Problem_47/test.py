# Problem: Buggy: Count Evens
# Difficulty: 3
# Topic: Debugging
#
# This function is SUPPOSED to count how many even numbers are in the
# list, but someone introduced a bug. Find it and fix it -- don't
# rewrite the function from scratch.
#
# Example:
#     numbers = [1, 2, 3, 4, 5, 6]  ->  3

def run(numbers):
    count = 0
    for n in numbers:
        if n % 2 == 1:
            count += 1
    return count
