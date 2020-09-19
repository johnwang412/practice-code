#!/usr/bin/env python3

import functools
import math
import os
import random
import re
import sys


# os.environ['OUTPUT_PATH'] = './output.txt'


# Complete the getMinimumCost function below.
def getMinimumCost(num_friends, price_list):
    """
    # must buy all flowers so minimize multiples for highest cost first

    Algo
    # loop through friends, each time through loop:
    # - purchase flowers starting from most expensive
    # - prices increase at end of loop
    """

    price_list.sort()

    # print(f'num_friends: {num_friends}')
    num_needed = len(price_list)

    total_cost = 0
    flower_idx = len(price_list)
    multiple = 1
    while flower_idx > 0:
        start_idx = flower_idx-num_friends
        if start_idx < 0:
            start_idx = 0

        price_to_buy_list = price_list[start_idx:flower_idx]
        total_cost += functools.reduce(lambda x,y: x+y, map(lambda x: x*multiple, price_to_buy_list) )

        flower_idx -= num_friends
        multiple += 1
        # print(f'total_cost: {total_cost}')
    
    return total_cost


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nk = input().split()

    n = int(nk[0])

    k = int(nk[1])

    c = list(map(int, input().rstrip().split()))

    minimumCost = getMinimumCost(k, c)

    fptr.write(str(minimumCost) + '\n')

    fptr.close()

