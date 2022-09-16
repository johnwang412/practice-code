"""
Recursive implementation
"""
from typing import List


class Solution:

    candidates: List[int]
    target: int
    solution_list: List[List]

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        self.solution_list = []
        self.candidates = candidates
        self.target = target

        first_layer = [[c] for c in self.candidates]
        self.get_solutions(first_layer)

        return self.solution_list


    def get_solutions(self, existing_paths: List[List]):

        next_paths = []
        for path in existing_paths:
            path_val = sum(path)
            if path_val == self.target:
                self.add_solution(path)
            elif path_val < self.target:
                for c in self.candidates:
                    if path_val + c < self.target:
                        next_paths.append(path+[c])
                    elif path_val + c == self.target:
                        self.add_solution(path+[c])
        if next_paths:
            self.get_solutions(next_paths)

    def add_solution(self, solution: List[int]):
        solution.sort()
        if solution not in self.solution_list:
            self.solution_list.append(solution)


s = Solution()

solution = s.combinationSum([7,3,2], 18)
print(solution)
