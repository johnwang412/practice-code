"""
Optimize solution 4 by preprocessing list but maintaining array indexing ability
"""
import pdb
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        if len(nums) == 0 or len(nums) == 1:
            return 0

        master_list = preprocess(nums)

        # don't look back further than the biggest number
        # TODO: this was a cheap hack and falls apart when numbers are large
        max_lookback = max(master_list)

        # paths through master list composed of indexes
        paths: List[List] = [[len(master_list)-1]]

        while True:

            new_paths = {}
            while paths:
                """
                For each path, take the lowest indexed "stop" on the path and
                create a new path for any lower indexed "stops" that can reach
                it
                """
                path = paths.pop()
                target_idx = path[-1]
                # iterate through all ower "stops"
                i = max(0, target_idx - max_lookback)
                while i < target_idx:
                    if master_list[i] != -1:
                        if i + master_list[i] >= target_idx:
                            if i == 0:
                                return len(path)

                            # This "stop" can reach the target in 1 step so append
                            # a new path
                            if i not in new_paths:
                                new_paths[i] = path + [i]
                            else:
                                if len(path) + 1 < len(new_paths[i]):
                                    new_paths[i] = path + [i]

                    i += 1
            for _, path in new_paths.items():
                paths.append(path)


def preprocess(input_list):
    dominant_pairs = [(0, input_list[0])]

    for idx, n in enumerate(input_list):
        if n == 0:
            input_list[idx] = -1

        pair_is_dominant = True
        for d_pair in dominant_pairs:
            if idx > d_pair[0] and idx + n <= d_pair[0] + d_pair[1]:
                pair_is_dominant = False
                input_list[idx] = -1
                break
        if pair_is_dominant:
            dominant_pairs.append((idx, n))
    return input_list


print(f'******** RUNNING TESTS')

s = Solution()

input_list = [8,2,4,4,4,9,5,2,5,8,8,0,8,6,9,1,1,6,3,5,1,2,6,6,0,4,8,6,0,3,2,8,7,6,5,1,7,0,3,4,8,3,5,9,0,4,0,1,0,5,9,2,0,7,0,2,1,0,8,2,5,1,2,3,9,7,4,7,0,0,1,8,5,6,7,5,1,9,9,3,5,0,7,5]
expected = 13
res = s.jump(input_list)
assert res == expected, f'{res} is not min number of jumps'

