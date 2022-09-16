"""
Way too slow
"""
from typing import List


class Solution:

    """
    Target number

    1. Identify 'building blocks' from input set
    2. Sort and go down building blocks - for each block that is less than
       `target`, enumerate using it or not using it, and then iterate over
       combinations of smaller blocks to get to final combination.


    approach 1: generate all combinations from candidates
    """

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:


        candidates.sort(reverse=True)  # largest to smallest
        max_idx = len(candidates) - 1

        list_size = 1

        solution_list = []

        while not limit_reached(list_size, target, candidates[-1]):

            num_to_pick = list_size

            # picking candidate lists of length `list_size` to add up to target
            tracking_stack = [0] * num_to_pick

            while not all_combos_found(tracking_stack, max_idx):
                if target_reached(tracking_stack, candidates, target):
                    add_solution(solution_list, tracking_stack, candidates)
                # generate next combo
                increment_stack(tracking_stack, max_idx)

            list_size += 1

        return solution_list


def add_solution(solution_list, tracking_stack, candidates):
    solution = []
    for idx in tracking_stack:
        solution.append(candidates[idx])

    solution.sort()
    if solution not in solution_list:
        solution_list.append(solution)


def all_combos_found(tracking_stack: List, max_idx: int) -> bool:
    # "bottom" of stack is > maximum position
    return tracking_stack[0] > max_idx


def increment_stack(tracking_stack: List, max_idx):

    if sum(tracking_stack) == len(tracking_stack) * -1:
        for idx in range(0, len(tracking_stack)):
            tracking_stack[idx] = 0
        return

    stack_idx = len(tracking_stack) - 1  # start at the last item
    # Find first item on stack that can be incremented
    while stack_idx > 0:
        if tracking_stack[stack_idx] < max_idx:
            break
        stack_idx -= 1
    # Increment the stack_idx and set other idx behind it to 0
    tracking_stack[stack_idx] += 1
    stack_idx += 1
    while stack_idx < len(tracking_stack):
        tracking_stack[stack_idx] = 0
        stack_idx += 1


def limit_reached(list_size, target, smallest_candidate):
    return list_size * smallest_candidate > target


def target_reached(tracking_stack, candidates, target):
    total = 0
    for candidate_idx in tracking_stack:
        total += candidates[candidate_idx]

    return target == total


s = Solution()

# NOTE: way to slow for this case
# s.combinationSum([5,10,8,4,3,12,9], 27)

solution = s.combinationSum([2,3,6,7], 7)
expected = [[2,2,3],[7]]

assert solution == expected, f'{solution} != {expected}'
print(f'Completed successfully')

