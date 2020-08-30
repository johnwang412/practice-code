#!/usr/bin/env python3

import math
import os
import random
import re
import sys


def calc_sum(arr, row, col):
    my_sum = \
          arr[row+0][col+0] \
        + arr[row+0][col+1] \
        + arr[row+0][col+2] \
        + arr[row+1][col+1] \
        + arr[row+2][col+0] \
        + arr[row+2][col+1] \
        + arr[row+2][col+2]   
    return my_sum


# Complete the hourglassSum function below.
def hourglassSum(arr):

    row = 0
    col = 0
    max_sum = None

    while row+2 < len(arr):

        while col+2 < len(arr[0]):
            hr_sum = calc_sum(arr, row, col)
            if max_sum is None or hr_sum > max_sum:
                max_sum = hr_sum
            col += 1

        col = 0
        row += 1

    return max_sum


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))

    result = hourglassSum(arr)

    fptr.write(str(result) + '\n')

    fptr.close()

