#!/usr/bin/env python3
"""
https://www.hackerrank.com/challenges/angry-children-2
"""

import json
import typing


# NOTE: not working -- approach wrong
# 
# Alternate approach (from comments)
# - sort values
# - go down sorted array and take clusters of K elements
#   - find min of all clusters


class PacketSet:
    """Set of packets chosen to give to kids
    """
    def __init__(self, initial_set: typing.List):
        self.packet_list: typing.List = initial_set
        self.packet_diff_map: typing.Dict = {}
        self._set_initial_diffs()

    def __str__(self):
        d = {
            'packet set': self.packet_list,
            'diff': self.get_total_diff_abs(),
            'diff map': self.packet_diff_map,
        }
        return f'{json.dumps(d, indent=2)}'

    def _calc_diff_ith_el(self, i: int, new_packet_size: int):
        item_diff = new_packet_size - self.packet_list[i]
        num_pairs = len(self.packet_list) - 1 - i
        return self.packet_diff_map.get(i, 0) + num_pairs * item_diff

    def _calc_diff_other_el(self, i: int, new_packet_size: int):
        item_diff = new_packet_size - self.packet_list[i]
        return self.packet_diff_map[i] - item_diff

    def _calc_potential_diff(self, i: int, new_packet_size: int):
        """Return potential updated diff of replacing ith element with new 
        packet
        """
        ith_item_diff = self._calc_diff_ith_el(i, new_packet_size)

        idx = 0
        other_diffs_total = 0
        while idx < i:
            new_idx_diff = self._calc_diff_other_el(idx, new_packet_size)
            other_diffs_total += new_idx_diff
            idx += 1

        return abs(other_diffs_total + ith_item_diff)

    def _set_initial_diffs(self):
        """Calc initial total diffs for each item (except last)

        total diff is sum of (i - x) where i is item who's total diff
          we want to calculate
        Should only be run once in constructor
        """
        if not self.packet_list: 
            return
        i = 0
        while i < len(self.packet_list) - 1:
            j = i + 1

            num_neg = 0
            num_pos = 0
            neg_total = 0
            pos_total = 0
            total_diff = 0

            while j < len(self.packet_list):
                diff = self.packet_list[i] - self.packet_list[j]
                if diff < 0:
                    num_neg += 1
                    neg_total += diff
                else:
                    num_pos += 1
                    pos_total += diff
                total_diff += diff
                j += 1

            # todo: reflect everywhere
            self.packet_diff_map[i] = {
                'num_neg': num_neg,
                'num_pos': num_pos,
                'neg_total': neg_total,
                'pos_total': pos_total,
                'total_diff': total_diff,
            }

            i += 1

    def _set_new_packet(self, min_sub_idx: int, new_packet_size: int):
        # set new packet in the list
        self.packet_list[min_sub_idx] = new_packet_size

        # set diff for new packet element
        self.packet_diff_map[min_sub_idx] = self._calc_diff_ith_el(min_sub_idx, new_packet_size)
        # set diff for other elements
        idx = 0
        other_diffs_total = 0
        while idx < min_sub_idx:
            self.packet_diff_map[idx] = self._calc_diff_other_el(idx, new_packet_size)
            idx += 1

    def get_total_diff_abs(self):
        return abs(sum(self.packet_diff_map.values()))

    def try_adjustment(self, new_packet_size: int):
        """Try substituting packet_size into existing set
        
        If substituting packet_size into the existing set gives a lower total
        diff, then persist the adjustment
        """
        print(f'initial list: {self.packet_list}')
        min_diff_abs = self.get_total_diff_abs()
        min_sub_idx = None

        for i in range(0, len(self.packet_list)):
            potential_diff_abs = abs(self._calc_potential_diff(i, new_packet_size))
            if potential_diff_abs < min_diff_abs:
                min_diff_abs = potential_diff_abs
                min_sub_idx = i
                print(f'better diff - pkt:{new_packet_size} idx:{i} diff:{potential_diff_abs}')
        
        if min_sub_idx is not None:
            self._set_new_packet(min_sub_idx, new_packet_size)
        print()


def angryChildren(k, packets):
    """
    L: list of packets

    min(L) = min(L-1) 
    - include Lth item

        packets = [3,3,4,5,7,9,10]
                   x x x   L          
        
        minSet(L-1) = [3,3,4] which is the set in [3,3,4,5] that yields 
            minDiff
        
        Prove that substituting Lth element into minSet(L-1) will yield 
            minDiff(L)
          
            Proof: substituting any other excluded ith element in L does not 
            work

    - exclude Lth item: just min(L-1)

    mem data structure:
    - key: ith index representing sublist from 0 to i in packets
    - value:
        - 

    algo:
    1. given Lth item, iterate through minSet(L-1)
        - check minDiff of resulting set
            PERF

    2. start with initial K set
        - for each element, keep total diff wrt other elements
            - total diff is not abs - can be negative
                assuming set is [3,4,3,4], first entry will be 
                - 3: 4, 3, 4 --> -2
                - 4: 3, 3, 4 -->  2

        - given new element, try substituting for each i set K
            Example: replace 3 with 5 for first two entries:
                - 3->5: 4, 3, 4 --> -2 + (5-3)*3 = 4
                - 4: 3->5, 3, 4 -->  2 - (5-3) = 0
                

    """
    if len(packets) < k:
        raise Exception(f'too many kids, Bill Gates out')

    p_set = PacketSet(packets[0:k])

    next_idx = k
    while next_idx < len(packets):
        p_set.try_adjustment(packets[next_idx])
        next_idx += 1

    print(f'p_set: {p_set}')
    return p_set.get_total_diff_abs()


def main():

    k = 3
    packets = [3,3,9,5,7,4,10]

    """

    track how many negative + negative total
    track how many positive + positive total

    3,3,9

    3: 3, 9 --> 0, -6  = 6
    3: 9    --> -6     = 6

    3->5: 3, 9 --> 0 + 2, -6 + 2  = 
    3->5: 9    --> -6     = 6
    """


    #          x x x   L          
    # 
    # Prove that substituting L into minSet(L-1) will yield min(L)
    # - substituting any other excluded packet in L does not work

    print(f'min: {angryChildren(k, packets)}')

if __name__ == '__main__':
    main()

