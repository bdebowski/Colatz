import random
from typing import List


class Solution:
    @staticmethod
    def as_string(s: List[int]):
        return "".join(str(i) for i in s)

    @staticmethod
    def rand(num_bits=20):
        """
        Generate random solution of length specified.
        Solutions are binary strings represented as lists of integers.
        """
        n = random.randint(1, 2 ** num_bits - 1)
        return [int(i) for i in "{:0{}b}".format(n, num_bits)]

    @staticmethod
    def mutate(s: List[int], r=0.1):
        """
        Mutate in-place at rate specified by r.
        """
        for i in range(len(s)):
            if random.random() <= r:
                s[i] ^= 1  # flip bit

    @staticmethod
    def cross(s1: List[int], s2: List[int], r=0.75):
        """
        Generate two children either by:
          a) copying the parents or
          b) crossing s1 and s2 at the midpoint.
        Crossover happens at a rate specified by r.
        """
        if random.random() <= r:
            crossover_index = len(s1) // 2
            child1 = s1[:crossover_index] + s2[crossover_index:]
            child2 = s2[:crossover_index] + s1[crossover_index:]
        else:
            child1 = s1.copy()
            child2 = s2.copy()
        return child1, child2

    @staticmethod
    def repair(s: List[int]):
        """
        Checks for and repairs the case where all bits are 0.
        Repair by setting last bit to 1.
        """
        if sum(s) == 0:
            s[-1] = 1
