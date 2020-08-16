#!/bin/python


def doit(n, arr):
    return arr


if __name__ == "__main__":
    n = long(raw_input().strip())
    arr_str = raw_input().strip()
    print doit(n, arr_str.split(' '))
