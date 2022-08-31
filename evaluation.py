from typing import List
import math

from solution import Solution


def apply_colatz(n: int, limit: int = 10000):
    """
    Apply the colatz pattern repeatedly until we reach terminal state of 1 (or num steps exceeds the limit):
      If n is even we divide it by 2, else we multiply n by 3 and add 1
    """
    if n < 1:
        raise ValueError("n must be integer greater than or equal to 1")

    hist = [n]
    while 1 < n and len(hist) < limit:
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
        hist.append(n)
    return hist


def evaluate_soln(s: List[int]):
    """
    Evaluate the fitness of a solution s.
    f = ln(num_steps_resulting_from_s) / (1.0 + ln(s_as_int))
    """
    s_int = int(Solution.as_string(s), 2)
    #return math.log(len(apply_colatz(s_int))) / (1.0 + math.log(s_int))
    #return math.log(len(apply_colatz(s_int)))
    return len(apply_colatz(s_int)) / 10000
    #return s_int
