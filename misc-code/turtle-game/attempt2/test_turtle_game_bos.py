import pytest

from turtle_game_bo import Board, Turtle, Direction


@pytest.mark.parametrize(
    "height, width, expected_rows, expected_cols",
    [
        (4, 3, 4, 3),  # Standard case
        (1, 1, 1, 1),  # Minimal dimensions
        (2, 5, 2, 5),  # Wider than tall
        (5, 2, 5, 2),  # Taller than wide
        (0, 0, 0, 0),  # Taller than wide
        (-1, 0, 0, 0),
        (0, -1, 0, 0),

    ]
)
def test_board_init(height, width, expected_rows, expected_cols):
    if height < 0 or width < 0:
        with pytest.raises(Exception):
            Board(width, height)
        return

    board = Board(width, height)
    assert len(board.matrix) == expected_rows
    if expected_rows > 0:
        assert len(board.matrix[0]) == expected_cols


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (2, 2, True),    # Valid in-bounds position
        (-1, 0, False),  # Out of bounds (negative x)
        (0, -1, False),  # Out of bounds (negative y)
        (5, 0, False),   # Out of bounds (x too large)
        (0, 5, False),   # Out of bounds (y too large)
    ]
)
def test_board_is_open(x, y, expected):
    board = Board(5, 5)
    assert board.is_open(x, y) is expected


def test_turtle_moves_on_board():
    board = Board(3, 3)
    turtle = Turtle(0, 0, board)
    # Move right (should succeed)
    assert turtle.move(Direction.RIGHT) is True
    assert turtle.get_position() == (1, 0)
    # Move down (should fail, cell is occupied)
    assert turtle.move(Direction.DOWN) is False
    assert turtle.get_position() == (1, 0)
    # Move right (should succeed)
    assert turtle.move(Direction.RIGHT) is True
    assert turtle.get_position() == (2, 0)
    # Move down (should succeed)
    assert turtle.move(Direction.DOWN) is False
    assert turtle.get_position() == (2, 0)
    # Move left (should succeed)
    assert turtle.move(Direction.LEFT) is True
    assert turtle.get_position() == (1, 0)
    # Move down (should succeed)
    assert turtle.move(Direction.UP) is True
    assert turtle.get_position() == (1, 1)


@pytest.mark.parametrize(
    "direction, expected, position",
    [
        (Direction.UP, False, (0,0)),
        (Direction.DOWN, False, (0,0)),
        (Direction.LEFT, False, (0,0)),
        (Direction.RIGHT, False, (0,0)),
    ]
)
def test_turtle_move_prison_board(direction, expected, position):
    """
    1x1 board where turtle can't move anywhere
    """
    board = Board(1, 1)
    turtle = Turtle(0, 0, board)
    # Move right (should succeed)
    assert turtle.move(direction) == expected
    assert turtle.get_position() == position


@pytest.mark.parametrize(
    "turtle_pos, obstacles, direction, expected, position",
    [
        ((0,0), [(0,1), (1,0), (1,1)], Direction.UP, False, (0,0)),
        ((0,0), [(0,1), (1,0), (1,1)], Direction.RIGHT, False, (0,0)),
        ((1,1), [(0,0), (0,1), (1,0)], Direction.DOWN, False, (1,1)),
        ((1,1), [(0,0), (0,1), (1,0)], Direction.LEFT, False, (1,1)),
    ]
)
def test_turtle_move_prison_board(turtle_pos, obstacles, direction, expected, position):
    """
    1x1 board where turtle can't move anywhere
    """
    board = Board(2, 2, obstacles)
    turtle = Turtle(turtle_pos[0], turtle_pos[1], board)
    # Move right (should succeed)
    assert turtle.move(direction) == expected
    assert turtle.get_position() == position
