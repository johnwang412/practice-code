#!/usr/bin/env python3  

import math
import os
import random
import re
import sys
import typing


def upper_case_last(a):
    return a[:-1] + a[-1:].upper()

def is_no_caps(a):
    for i in range(0, len(a)):
        if ord(a[i]) < 97:
            return False
    return True


def is_cap(letter):
    if len(letter) > 1:
        raise Exception(f'{letter} is not valid letter')
    return ord(letter) < 97


def abbr_helper(a, b, mem: typing.Dict) -> str:
    """
    daBcd
    ABC

    daBFcd
    ABC
    """
    a_idx = len(a) - 1 
    b_idx = len(b) - 1
    success = 'NO'
    finished = False
    stack = []

    while not finished:

        # if pop_stack=True, then we've run into fail case so see if there is 
        # an index pair on the stack to check
        pop_stack = False

        if (a_idx, b_idx) in mem:
            pop_stack = True

        if not pop_stack:

            # Check if immediate fail or pass
            if b_idx < 0 and a_idx >= b_idx:
                # if we've gone through all of b string
                success = 'YES'
                finished = True
                continue
            elif a_idx < b_idx:
                mem[(a_idx, b_idx)] = 'F'
                pop_stack = True
        
            """
            if A-last is capitalized
                compare
                    if success, then a--, b-- and proceed
                    if fail, then fail

            if A-last not capitalized,
                capitalize and compare
                    if success, then skip both
                    if fail, then a-- and proceed
                do not capitalize
                    then a-- and proceed

            mem is (a_idx, b_idx)
            """
            a_last = a[a_idx:a_idx+1]
            b_last = b[b_idx:b_idx+1]
            if is_cap(a_last):
                if a_last == b_last:
                    if (a_idx-1, b_idx-1) in mem:
                        mem[(a_idx, b_idx)] = 'F'
                        pop_stack = True
                    else:
                        a_idx -= 1
                        b_idx -= 1
                else:
                    mem[(a_idx, b_idx)] = 'F'
                    pop_stack = True
            else:
                if a_last.upper() == b_last and (a_idx-1, b_idx-1) not in mem:
                    if (a_idx-1, b_idx) not in mem:
                        stack.append((a_idx-1, b_idx))
                    a_idx -= 1
                    b_idx -= 1
                else:
                    if (a_idx-1, b_idx) not in mem:
                        a_idx -= 1
                    else:
                        mem[(a_idx, b_idx)] = 'F'
                        pop_stack = True


        if pop_stack:
            if len(stack) > 0:
                a_idx, b_idx = stack.pop()
            else:
                finished = True

    return success


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

