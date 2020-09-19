#!/usr/bin/env python3

import math
import os
import random
import re
import sys


# Complete the maxMin function below.
def maxMin(k, arr):
    """
    ideas:
    - find delta between all integers and include progressively 
    larger deltas until all k slots filled in new array

    - start with initial arr of k, sort elements -> bring new 
    element in -> if that is better, then keep

    - sort array -> keep moving down window of length k until
    we find min
      - winner: try this
    """

    arr.sort()
    delta = None

    if k > len(arr):
        raise Exception(f'k > length of arr -- should not hit this condition')
    
    end_idx = k-1
    while end_idx < len(arr):
        new_delta = arr[end_idx] - arr[end_idx-k+1]
        if delta is None or new_delta < delta:
            delta = new_delta

        end_idx += 1

    return delta


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    k = int(input())

    arr = []

    for _ in range(n):
        arr_item = int(input())
        arr.append(arr_item)

    result = maxMin(k, arr)

    fptr.write(str(result) + '\n')

    fptr.close()


