#!/bin/python3

import json
import math
import os
import random
import re
import sys
import typing


class SumMem:

    def __init__(self):
        self.sum_map = {}

    def __str__(self):
        return f'{json.dumps(self.sum_map, indent=2)}'

    def _get_key(self, len_idx: int) -> str:
        return str(len_idx)

    def get_max_subset_sum(self, len_idx: int) -> typing.Optional[int]:
        """len_idx is treated as the key

        len_idx is the index into the array representing the sub array 
        starting at 0
        """
        key_str = self._get_key(len_idx)
        entry = self.sum_map.get(key_str, None)
        if not entry:
            return None
        return entry['max_subset_sum']

    def get_max_values(self, len_idx: int) -> typing.Optional[int]:
        key_str = self._get_key(len_idx)
        entry = self.sum_map.get(key_str, None)
        if not entry:
            return None
        return entry['max_values']

    def set(self, len_idx: int, max_subset_sum: int, max_values: int):
        """
        :param max_values: max of the values in the array so we don't have to 
            find max again; used in _get_max_pairs
        """
        key_str = self._get_key(len_idx)
        self.sum_map[key_str] = {
            'max_subset_sum': max_subset_sum,
            'max_values': max_values,
        }


def _get_max(input_arr, next_idx, mem) -> typing.Tuple[int, int]:
    """
    Logic

    L  = [A, B, C-X]

    max(L) = A+max([C-X]), max([B,C-X]), max(pair A with each item in [C-X])
    """
    if len(input_arr) < 3:
        raise Exception(
            f'cannot call _get_max with input_arr of length: {len(input_arr)}')

    new_val = input_arr[next_idx]

    # get max of pairs
    max_of_pair_arr = mem.get_max_values(next_idx - 2)
    max_pairs = new_val + max_of_pair_arr

    # get max_with new value
    max_with = max_pairs  # if 
    if mem.get_max_subset_sum(next_idx - 2) is not None:
        max_with = new_val + mem.get_max_subset_sum(next_idx - 2)
    # get max without new value
    max_without = max_pairs  # 
    if mem.get_max_subset_sum(next_idx - 1) is not None:
        max_without = mem.get_max_subset_sum(next_idx - 1)

    return \
        max(max_pairs, max_with, max_without), \
        max(new_val, mem.get_max_values(next_idx - 1))


def max_subset_sum(input_arr: typing.List, mem: SumMem) -> int:
    """
    Logic

    L  = [A, B, C-X]

    max(L) = A+max([C-X]), max([B,C-X]), max(pair A with each item in [C-X])
    """
    if not input_arr or len(input_arr) < 3:
        return 0

    # base case --> arr of length 3 is max sum of elements at 0 and 2 idx
    max_sum = input_arr[0] + input_arr[2]
    mem.set(2, max_sum, max(input_arr[0:3]))
    # set max sum for other base cases
    mem.set(0, None, max(input_arr[0:1]))
    mem.set(1, None, max(input_arr[0:2]))

    next_idx = 3
    while next_idx < len(input_arr):
        this_subset_sum, max_values = _get_max(input_arr, next_idx, mem)

        max_sum = max(this_subset_sum, max_sum)
        mem.set(next_idx, max_sum, max_values)

        next_idx += 1

    return max_sum


def maxSubsetSum(arr):
    mem = SumMem()
    return max_subset_sum(arr, mem)


def main():

    input_arr = [3,7,4,6,5]
    input_arr = [-2, 1, 3, -4, 5]
    input_arr = [2,1,5,8,4]

    print(f'max subset sum: {maxSubsetSum(input_arr)}')


if __name__ == '__main__':
    main()

