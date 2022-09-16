"""
Works and is fast enough.

Memory and speed is terrible.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Pair:
    candidate_value: int
    num: int


class Solution:
    """
    """

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        candidates.sort(reverse=True)  # largest to smallest

        # Incomplete solutions are those that can still be built up
        possible_solutions = []
        for op_idx in range(0, len(candidates)):

            cand_val = candidates[op_idx]

            # add to existing solution lists that can take this candidate val without going over
            new_possible_solutions = []
            for possible_sol in possible_solutions:
                sol_sum = _get_sum(possible_sol)
                delta = target - sol_sum

                if delta > 0 and cand_val <= delta:
                    # there is a delta to fill and we can fill it with candidate value

                    # create a new possible solutions when we can add more than 1 cand_val
                    num_cand_val = 1
                    while delta >= num_cand_val * cand_val:
                        new_sol = []
                        for item in possible_sol:
                            new_sol.append(Pair(item.candidate_value, item.num))
                        new_sol.append(Pair(cand_val, num_cand_val))
                        num_cand_val += 1
                        new_possible_solutions.append(new_sol)

            # add solution lists that just start with this candidate val
            quotient = int(target / cand_val)
            remainder = target % cand_val
            for x in range(1, quotient + 1):
                possible_solutions.append([Pair(cand_val, x)])

            # add on new possible solutions
            for sol in new_possible_solutions:
                possible_solutions.append(sol)

        solution_list = []
        for sol in possible_solutions:
            if _get_sum(sol) == target:
                solution_list.append(_to_int_array(sol))

        solution_list.sort()
        return solution_list


def _get_sum(possible_sol: List[Pair]) -> int:
    total = 0
    for pair in possible_sol:
        total += pair.candidate_value * pair.num
    return total


def _to_int_array(solution: List[Pair]) -> List[int]:
    arr = []
    for pair in solution:
        for i in range(0, pair.num):
            arr.append(pair.candidate_value)
    arr.sort()
    return arr


s = Solution()

s.combinationSum([5,10,8,4,3,12,9], 27)
solution = s.combinationSum([2,3,6,7], 7)
expected = [[2,2,3],[7]]

assert solution == expected, f'{solution} != {expected}'
print(f'Completed successfully')


