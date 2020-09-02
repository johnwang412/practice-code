#!/usr/bin/env python3

import math
import os
import random
import re
import sys


# Complete the largestRectangle function below.
def largestRectangle_1(h: list):

    # is there a math equation that does this

    rect_map = {}

    for i in range(0,len(h)):

        # add i_idx as entry in rect_map (with 1 height)
        i_height = h[i]
        area_so_far = i_height
        # gather preceding rect contributions to i_idx
        # - if i is <= preceding rectangle
        preceding_idx = i-1
        while preceding_idx >= 0:
            if h[preceding_idx] >= i_height:
                area_so_far += i_height
            else:
                break
            preceding_idx -= 1
        rect_map[i] = area_so_far
        

        # see if i_idx can contribute to any rectangles preceding it
        # - if i is >= preceding rectangle, contribute preceding rect height
        preceding_idx = i-1
        min_height_seen = i_height
        while preceding_idx >= 0:

            if h[preceding_idx] <= i_height:
                # i_height might contribute to rectangle of preceding_idx
                if h[preceding_idx] <= min_height_seen:
                    rect_map[preceding_idx] += h[preceding_idx]

            if h[preceding_idx] < min_height_seen:
                min_height_seen = h[preceding_idx]

            preceding_idx -= 1

    return max(rect_map.values())


# Complete the largestRectangle function below.
def largestRectangle_2(h: list):

    # is there a math equation that does this

    max_area = 0

    for i in range(0,len(h)):

        area_so_far = h[i]

        j = i-1
        while j >= 0:
            if h[j] >= h[i]: 
                area_so_far += h[i]
            else:
                break
            j -= 1
        
        j = i + 1
        while j < len(h):
            if h[j] >= h[i]: 
                area_so_far += h[i]
            else:
                break
            j += 1
        
        if max_area < area_so_far:
            max_area = area_so_far


    return max_area


# Complete the largestRectangle function below.
def largestRectangle(h: list):
    if len(h) <= 0:
        return 0

    largest_area = 0

    first_pair = {
        'idx': 0,
        'height': h[0],
        'area': h[0],
    }
    tracking_stack = [first_pair]

    for i in range(1, len(h)):
        # drill down stack and dequeue higher buildings
        while len(tracking_stack) > 0:
            height = tracking_stack[-1]['height']
            if height > h[i]:
                item = tracking_stack.pop()
                if item['area'] > largest_area:
                    largest_area = item['area']
            else:
                break

        # accumulate h[j] for all buildings left on stack
        for j in range(0, len(tracking_stack)):
            tracking_stack[j]['area'] += tracking_stack[j]['height']

        # accumulate area for this building and push on to stack
        idx = 0
        if len(tracking_stack) > 0:
            j = len(tracking_stack) - 1
            while j >= 0:
                if tracking_stack[j]['height'] < h[i]:
                    break
                j -= 1
            idx = tracking_stack[j]['idx'] + 1
        i_area = (i - idx) * h[i] + h[i]
        # print(f'h[i]:{h[i]}   area:{i_area}')
        tracking_stack.append({
            'idx': i,
            'height': h[i],
            'area': i_area,
        })
    
    while len(tracking_stack) > 0:
        item = tracking_stack.pop()
        if item['area'] > largest_area:
            largest_area = item['area']

    return largest_area


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    h = list(map(int, input().rstrip().split()))

    result = largestRectangle(h)

    fptr.write(str(result) + '\n')

    fptr.close()


