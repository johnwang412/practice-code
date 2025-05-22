from dataclasses import dataclass, field

class Board:
    """
    Class to represent the board.
    Board is a 2D array of size (width, height). Board's lower left corner is
    at (0,0) and upper right corner is at (width-1, height-1).
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]

    def is_open_pos(self, coord):
        """Check if the position is open on the board."""
        x, y = coord
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False


@dataclass
class Turtle:
    x: int
    y: int
    board: Board

    # Class variables for keyboard directions
    UP: str = field(default='up', init=False, repr=False)
    DOWN: str = field(default='down', init=False, repr=False)
    RIGHT: str = field(default='right', init=False, repr=False)
    LEFT: str = field(default='left', init=False, repr=False)

    def __str__(self):
        return f"Turtle at ({self.x}, {self.y})"

    def move(self, direction):
        """Move the turtle
        :return: True if the turtle moved, False if it didn't.
        """
        new_coord = None
        if direction == self.UP:
            new_coord = (self.x, self.y + 1)
        elif direction == self.DOWN:
            new_coord = (self.x, self.y - 1)
        elif direction == self.RIGHT:
            new_coord = (self.x + 1, self.y)
        elif direction == self.LEFT:
            new_coord = (self.x - 1, self.y)
        else:
            return False

        if self.board.is_open_pos(new_coord):
            self.x, self.y = new_coord
            return True
        return False
