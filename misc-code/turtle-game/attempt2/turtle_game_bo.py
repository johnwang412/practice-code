from enum import Enum

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class Board:
    """
    Manages coordinates and how they are ordered.

    0,0 represents bottom left of board
    """
    def __init__(self, cols: int, rows: int, obstacles: list[tuple[int, int]]=None):
        """
        :param obstacles: obstacles coordinate list, (col, row)
        """
        if cols < 0 or rows < 0:
            raise Exception('Invalid board dimensions')
        self.matrix = [[1 for _ in range(cols)] for _ in range(rows)]
        if obstacles is not None:
            for obstacle in obstacles:
                self.matrix[obstacle[1]][obstacle[0]] = 0

    def is_open(self, col: int, row: int) -> bool:
        if 0 <= col < len(self.matrix[0]) and 0 <= row < len(self.matrix):
            return self.matrix[row][col] == 1
        return False

class Turtle:
    def __init__(self, col: int, row: int, board: Board):
        self.col = col
        self.row = row
        self.board = board
        if not board.is_open(self.col, self.row):
            raise Exception(f'Cannot place turtle on board at position ({self.col}, {self.row})')

    def move(self, direction: Direction):
        new_col, new_row = self.col, self.row
        if direction == Direction.UP:
            new_row += 1
        elif direction == Direction.DOWN:
            new_row -= 1
        elif direction == Direction.LEFT:
            new_col -= 1
        elif direction == Direction.RIGHT:
            new_col += 1
        if self.board.is_open(new_col, new_row):
            self.col, self.row = new_col, new_row
            return True
        return False

    def get_position(self):
        return self.col, self.row