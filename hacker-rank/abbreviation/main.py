#!/usr/bin/env python3  

import math
import os
import random
import re
import sys


def upper_case_last(a):
    return a[:-1] + a[-1:].upper()

def is_no_caps(a):
    for i in range(0, len(a)):
        if ord(a[i]) < 97:
            return False
    return True


def abbr_helper(a, b, mem) -> str:
    if (a,b) in mem:
        return mem[(a,b)]

    res = 'NO'
    if len(b) == 0 and is_no_caps(a):
        res = 'YES'
    elif len(b) == 0:
        res = 'NO'
    elif len(a) == 0:
        res = 'NO'
    else:
        if a[-1] == b[-1]:
            res = abbr_helper(a[:-1], b[:-1], mem)
            if res == 'NO':
                sub_a = upper_case_last(a[:-1])
                res = abbr_helper(sub_a, b[:-1], mem)
        else:
            if ord(a[-1]) < 97:
                res = 'NO'
            else:
                res = abbr_helper(a[:-1], b, mem)
                if res == 'NO':
                    sub_a = upper_case_last(a[:-1])
                    res = abbr_helper(sub_a, b, mem)

    mem[(a,b)] = res
    return res


# Complete the abbreviation function below.
def abbreviation(a, b) -> str:
    mem = {}
    return abbr_helper(a, b, mem)


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())

    for q_itr in range(q):
        a = input()

        b = input()

        result = abbreviation(a, b)

        fptr.write(result + '\n')

    fptr.close()

