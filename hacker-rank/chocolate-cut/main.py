#!/bin/python

def num_pieces(k):
    w = int(k/2)
    h = w
    if k % 2 == 1:
        h += 1

    return w*h

if __name__ == "__main__":
    n = int(raw_input().strip())
    for i in xrange(n):
        k = int(raw_input().strip())
        print num_pieces(k)
