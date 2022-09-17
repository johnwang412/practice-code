"""
Optimize solution2 for speed

Approach:
    - Look ahead during add_paths by N hops

Still not fast enough
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
        _add_paths(
            working_paths, root_path=[], start_idx=0,
            master_list=nums)
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
                    _add_paths(
                        working_paths, path, sum(path),
                        master_list=nums)

        return min_jump


def _add_paths(working_paths, root_path, start_idx, master_list, look_depth=3):
    """Add paths favoring the path that will get to next biggest jump

    working_paths: all paths we're iterating on - just a global to add to at the end

    root_path: path we're going to enhance
    start_idx: idx of item right after last root_path item
    max_dist:

    """
    next_jump_range = master_list[start_idx]
    jump_increments = list(range(1, next_jump_range+1))
    max_jump_dist = [min(start_idx + (i) + master_list[start_idx+i], len(master_list)-1) for i in jump_increments]

    """
                        v
    input_list = [8,2,4,4,4,9,5,2,5,8,8,0,8,6,9,1,1,6,3,5,1,2,6,6,0,4,8,6,0,3,2,8,7,6,5,1,7,0,3,4,8,3,5,9,0,4,0,1,0]

                  0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0
    """

    for _ in range(0, look_depth):
        tmp_jump_dist = []
        for idx in max_jump_dist:
            jump_range = master_list[idx]
            if jump_range <= 0:
                tmp_jump_dist.append(idx)
                continue
            candidates = master_list[idx+1:idx+jump_range+1]
            if not candidates:
                tmp_jump_dist.append(idx)
                continue
            next_jump_dist_list = [idx + (i+1) + c for i, c in enumerate(candidates)]
            max_dist = max(next_jump_dist_list)
            tmp_jump_dist.append(min(max_dist, len(master_list)-1))
        max_jump_dist = tmp_jump_dist

    jump_pairs = list(zip(jump_increments, max_jump_dist))
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
