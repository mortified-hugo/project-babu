import numpy as np


#  Simple maths functions
def round_div(x, y):
    """Divided two ints x and y to get a round up int"""

    return int(round(x / y))


def percentage(part, total):
    """Gets a percentage representation up to two digits of a part of a total

    :param part: partial number - int, float
    :param total: total number - int, float

    :returns: float of the percentage"""
    return round(((part / total) * 100), 2)


def vote(base, delta, minimum):
    """Function for generating a number of votes based on a given base

    :param base: Contestant.base- int
    :param delta: round delta, defined by round, usually 10, 7 and 5 - int
    :param minimum: minimum number of votes a Contestant can receive, usually 2 - int

    :returns: number of votes - int"""
    return max(base + np.random.randint(-delta, delta + 1), minimum)


#  Round Functions
