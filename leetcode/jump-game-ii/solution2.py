"""
Optimize solution1 for speed
Still too slow for large case
"""
import pdb
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        """
        """
        if len(nums) == 1 or nums[0] == 0:
            return 0
        if nums[0] >= len(nums) - 1:
            return 1

        working_paths = []

        # add the first set of jumps, then iterate from there
        _add_paths(working_paths, root_path=[], start_idx=1, max_dist=nums[0], master_list=nums)
        # accumulator for successful jumps
        min_jump = 0

        # Favor the farthest jump first
        while working_paths:
            """ Depth first search traversal """
            path = working_paths.pop()

            if not min_jump or len(path)+1 < min_jump:
                if sum(path) + nums[sum(path)] >= len(nums) - 1:
                    if sum(path) >= len(nums) - 1:
                        min_jump = len(path)
                    else:
                        min_jump = len(path) + 1
                elif sum(path) < len(nums) - 1:
                    _add_paths(working_paths, path, sum(path)+1, nums[sum(path)], nums)

        return min_jump


def _add_paths(working_paths, root_path, start_idx, max_dist, master_list):
    """Add paths favoring the path that will get to next biggest jump
    """

    next_jump_max_list = master_list[start_idx:start_idx+max_dist]
    current_jump_increments = list(range(1, max_dist+1))
    jump_pairs = list(zip(current_jump_increments, next_jump_max_list))
    sorted_pairs = sorted(jump_pairs, key=lambda x: x[1]*100 + x[0])

    for p in sorted_pairs:
        working_paths.append(root_path + [p[0]])


s = Solution()
"""
input_list = [2,3,1,1,4]
expected = 2
res = s.jump(input_list)
assert res == expected, f'{res} is not min number of jumps'
input_list = [1,2]
expected = 1
res = s.jump(input_list)
assert res == expected, f'{res} is not min number of jumps'
input_list = [3,2,1]
expected = 1
res = s.jump(input_list)
assert res == expected, f'{res} is not min number of jumps'
input_list = [1]
expected = 0
res = s.jump(input_list)
assert res == expected, f'{res} is not min number of jumps'
"""

input_list = [8,2,4,4,4,9,5,2,5,8,8,0,8,6,9,1,1,6,3,5,1,2,6,6,0,4,8,6,0,3,2,8,7,6,5,1,7,0,3,4,8,3,5,9,0,4,0,1,0,5,9,2,0,7,0,2,1,0,8,2,5,1,2,3,9,7,4,7,0,0,1,8,5,6,7,5,1,9,9,3,5,0,7,5]
expected = 0
res = s.jump(input_list)
assert res == expected, f'{res} is not min number of jumps'

