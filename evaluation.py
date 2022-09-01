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

    longest_increasing_seq_len = 0
    current_increasing_seq_len = 0
    increasing_seq_start_val = n
    hist = [n]
    while 1 < n:
        if len(hist) >= limit:
            raise RuntimeError("Max sequence length of {} exceeded.".format(limit))
        if n % 2 == 0:
            n = n // 2

            if n < increasing_seq_start_val:
                increasing_seq_start_val = n
                current_increasing_seq_len = 0
            else:
                current_increasing_seq_len += 1
        else:
            n = n * 3 + 1

            current_increasing_seq_len += 1

        hist.append(n)

        if current_increasing_seq_len > longest_increasing_seq_len:
            longest_increasing_seq_len = current_increasing_seq_len

    return hist, longest_increasing_seq_len


def evaluate_soln(s: List[int]):
    """
    Evaluate the fitness of a solution s.
    f = ln(num_steps_resulting_from_s) / (1.0 + ln(s_as_int))
    """
    s_int = int(Solution.as_string(s), 2)
    #return math.log(len(apply_colatz(s_int))) / (1.0 + math.log(s_int))
    #return math.log(len(apply_colatz(s_int)))
    #return len(apply_colatz(s_int)) / 10000
    #return s_int
    _, len_chain = apply_colatz(s_int)
    return len_chain
