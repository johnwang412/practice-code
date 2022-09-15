from typing import List


# TODO: figure out where to store constants
LIVING = 1
DEAD = 0


class Solution:

    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """


        height = len(board)
        width = len(board[0])

        next_state = [[0]*width for _ in range(height)]

        for y in range(0, height):
            for x in range(0, width):
                num_neighbors = get_num_neighbors(board, x, y)
                existing_state = board[y][x]
                n_state = get_next_state(existing_state, num_neighbors)
                next_state[y][x] = n_state

        for y in range(0, height):
            for x in range(0, width):
                board[y][x] = next_state[y][x]


def get_num_neighbors(board: List[List[int]], x: int, y: int) -> int:

    # dupe calculation
    height = len(board)
    width = len(board[0])

    num_neighbors = 0
    for nx in range(x-1, x+2):
        for ny in range(y-1, y+2):
            if is_in_bounds(nx, ny, width, height):
                if nx != x or ny != y:
                    num_neighbors += board[ny][nx]
    return num_neighbors


def get_next_state(existing_state, num_neighbors) -> int:
    if is_living(existing_state):
        if num_neighbors in [2, 3]:
            return LIVING
        else:
            return DEAD

    # is_living is false
    if num_neighbors == 3:
        return LIVING
    return DEAD


def is_in_bounds(x, y, width, height):
    return x >= 0 and y >= 0 and x < width and y < height


def is_living(some_state: int) -> bool:
    return some_state == 1


# Runtime

s = Solution()
b = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]
s.gameOfLife(b)
solution = [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]
# solution = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]

if b == solution:
    print('correct')
else:
    print('incorrect')
