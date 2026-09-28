# Problem: Buggy: FizzBuzz
# Difficulty: 3
# Topic: Debugging
#
# This function is SUPPOSED to return "FizzBuzz" for multiples of 15,
# "Fizz" for multiples of 3, "Buzz" for multiples of 5, otherwise the
# number as a string -- but someone introduced a bug. Find it and fix it.
#
# Example:
#     n = 15  ->  "FizzBuzz"
#
# Notes:
#     Test it on 15 -- think carefully about WHY that case breaks, not just
#     how to patch it.

def run(n):
    if n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    elif n % 15 == 0:
        return "FizzBuzz"
    else:
        return str(n)
