"""
Works and is fast. Got the idea from a solution though. Need to be better about
simple iterative memoization.
"""
from typing import List


class Solution:

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()

        possible_solutions = [[c] for c in candidates]
        solutions = []
        print(possible_solutions)

        while len(possible_solutions) > 0:

            tmp_holding = []

            for sol in possible_solutions:

                delta = target - sum(sol)
                if delta <= 0:
                    if delta == 0:
                        solutions.append(sol)
                else:
                    for cand_val in candidates:
                        if cand_val + sum(sol) <= target and cand_val >= max(sol):
                            tmp_holding.append(sol + [cand_val])

            possible_solutions = tmp_holding

        return solutions


s = Solution()

solution = s.combinationSum([7,3,2], 18)
expected = [[2,2,3],[7]]
print(solution)


