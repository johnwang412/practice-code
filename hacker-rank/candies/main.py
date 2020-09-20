#!/usr/bin/env python3

import functools
import math
import os
import random
import re
import sys
import typing


def process_desc_start(arr, candies, desc_start, i):
    j = i - 1
    num_candies = 2
    while j >= desc_start:
        candies[j] = max(num_candies, candies[j])
        num_candies += 1
        j -= 1


# Complete the candies function below.
def candies(n: int, arr: typing.List):

    if n != len(arr):
        raise Exception(f'num children != num ratings')

    candies = [1] * n
    desc_start = None

    for i in range(1, len(arr)):

        if arr[i] >= arr[i-1] and desc_start is not None:
            process_desc_start(arr, candies, desc_start, i-1)
            desc_start = None

        if arr[i] > arr[i-1]: 
            candies[i] = candies[i-1]+1

        if arr[i] < arr[i-1] and desc_start is None:
            desc_start = i-1

    if desc_start is not None:
        process_desc_start(arr, candies, desc_start, len(arr)-1)
    
    return sum(candies)


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    arr = []

    for _ in range(n):
        arr_item = int(input())
        arr.append(arr_item)

    result = candies(n, arr)

    fptr.write(str(result) + '\n')

    fptr.close()

