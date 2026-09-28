# Problem: Buggy: Reverse a String
# Difficulty: 3
# Topic: Debugging
#
# This function is SUPPOSED to return a string reversed, but someone
# introduced a bug. Find it and fix it.
#
# Example:
#     text = "hello"  ->  "olleh"
#
# Notes:
#     Try it on a single-character string like "a" first -- that case makes
#     the bug very obvious.

def run(text):
    result = ""
    for i in range(len(text) - 1):
        result = text[i] + result
    return result
