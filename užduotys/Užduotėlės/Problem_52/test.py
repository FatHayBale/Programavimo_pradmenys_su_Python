# Problem: Buggy: Word Frequency (crashes!)
# Difficulty: 3
# Topic: Debugging (tracebacks)
#
# This function is SUPPOSED to count word frequencies, like the standard
# word frequency problem -- but it currently CRASHES with an error instead of just
# giving a wrong answer. Run it, read the traceback Python prints,
# and use it to figure out exactly which line and why it's failing.
#
# Example:
#     text = "the cat sat on the mat"  ->  {"the":2,"cat":1,"sat":1,"on":1,"mat":1}
#
# Notes:
#     This is real 'reading a traceback' practice: Python will tell you the
#     exact line and the exact error type (KeyError). Read it before guessing.

def run(text):
    words = text.lower().split()
    freq = {}
    for w in words:
        freq[w] = freq[w] + 1
    return freq
