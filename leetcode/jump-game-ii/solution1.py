"""
Seems to be correct solution, but time limit exceeded
"""
import pdb
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        """
        ex: [2,3,0,1,4]
        """

        # add the first set of jumps, then iterate from there
        max_dist = nums[0]
        working_paths = [[x] for x in range(1, max_dist+1)]
        # accumulator for successful jumps
        min_jump = []

        while working_paths:
            tmp_stack = []

            for path in working_paths:
                if not min_jump or len(path) < len(min_jump):
                    if sum(path) == len(nums) - 1:
                        min_jump = path
                    elif sum(path) < len(nums) - 1:
                        tmp_dist = nums[sum(path)]
                        for x in range(1, tmp_dist+1):
                            tmp_stack.append(path + [x])

            working_paths = tmp_stack

        return len(min_jump)


s = Solution()


res = s.jump([2,3,0,1,4])
expected = 2
assert res == expected, f'{res} is not min number of jumps'
