#!/bin/python

import math
import time


PRIMES_MAP = {}
PRIMES_LIST = [2, 3, 5, 7]


def do(x):
    # factor out 4
    if (x % 2) == 0:
        x //= 2
        if (x % 2) == 0:
            x //= 2

    # factor out 2s and 5s and make them equal (to power of 10)
    num_twos = 0
    num_fives = 0
    while x % 2 == 0:
        num_twos += 1
        x //= 2
    while x % 5 == 0:
        num_fives += 1
        x //= 5
    num_zeros = max(num_twos, num_fives)

    # Take the xprimes left over and find the smallest [1]+ number they can factor into
    candidate = 1
    num_fours = 1
    while candidate % x != 0:
        candidate = candidate * 10 + 1
        num_fours += 1

    return num_fours * 2 + num_zeros


def to_num(p_list):
    return reduce(lambda acc, x: x * acc, p_list, 1)

def try_match(val, x_primes, min_val):
    if val < min_val:
        return False, []
    val_primes = primes(val)

    # todo: optimize
    for xp in x_primes:
        if xp in val_primes:
            val_primes.pop(val_primes.index(xp))
        else:
            return False, []
    return True, val_primes


def primes(n):
    if n == 1:
        return []
    if n in PRIMES_MAP:
        return PRIMES_MAP[n][:]

    while True:
        for p in PRIMES_LIST:
            if n % p == 0:
                ret_list = [p] + primes(n / p)
                PRIMES_MAP[n] = ret_list
                return ret_list[:]
        add_next_prime(PRIMES_LIST)


def add_next_prime(plist):
    if len(plist) == 0:
        plist = [2]
        return

    candidate = plist[-1] + 1

    found = False
    while not found:
        tmp_cand = candidate
        for p in plist:
            while tmp_cand % p == 0:
                tmp_cand = long(tmp_cand / p)
        if tmp_cand == candidate:
            found = True
            plist.append(candidate)
        candidate += 1

    return


if __name__ == "__main__":
    n = long(raw_input().strip())
    for i in xrange(n):
        k = long(raw_input().strip())
        print do(k)
