#!/usr/bin/env python3

import functools
import math
import os
import random
import re
import sys
import typing


def _adjust_fairness(ratings_arr: typing.List, candies_arr: typing.List, idx: int):
    if idx <= 0: 
        return

    while idx > 0 \
            and ratings_arr[idx] < ratings_arr[idx-1] \
            and candies_arr[idx] >= candies_arr[idx-1]:

        candies_arr[idx-1] = candies_arr[idx] + 1
        idx -= 1


# Complete the candies function below.
def candies(num_children: int, ratings_arr: typing.List):

    candies_arr = []

    # ratings_arr: [2, 4, 3, 5, 2, 6, 4, 5]

    for idx in range(0, len(ratings_arr)):

        score = 1
        if idx > 0 and ratings_arr[idx] > ratings_arr[idx-1]:
            score = candies_arr[idx-1] + 1
        
        candies_arr.append(score)

        _adjust_fairness(ratings_arr, candies_arr, idx)

    return functools.reduce(lambda x, y: x+y, candies_arr, 0)


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

