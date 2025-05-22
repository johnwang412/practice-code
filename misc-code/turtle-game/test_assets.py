import pytest

import assets


@pytest.mark.parametrize(
    "directions, expected_x, expected_y",
    [
        ([assets.Turtle.UP, assets.Turtle.RIGHT, assets.Turtle.UP], 1, 2),   # up, right, up
        ([assets.Turtle.RIGHT, assets.Turtle.RIGHT, assets.Turtle.DOWN], 2, 0),   # right, right, down
        ([assets.Turtle.UP, assets.Turtle.LEFT, assets.Turtle.DOWN], 0, 0),   # up, left, down (returns to start)
        ([assets.Turtle.RIGHT, assets.Turtle.UP, assets.Turtle.RIGHT], 2, 1),   # right, up, right
        ([assets.Turtle.DOWN, assets.Turtle.DOWN, assets.Turtle.RIGHT], 1, 0),   # down, down (no effect at y=0), right
        ([assets.Turtle.UP, assets.Turtle.UP, assets.Turtle.UP], 0, 2),   # up, up, up (third up no effect)
        ([assets.Turtle.RIGHT, assets.Turtle.RIGHT, assets.Turtle.RIGHT], 2, 0),   # 3 rights - last one no effect
    ]
)
def test_turtle_move(directions, expected_x, expected_y):
    """
    Test the turtle's move method.
    """
    board = assets.Board(3, 3)
    turtle = assets.Turtle(0, 0, board)
    for d in directions:
        turtle.move(d)
    assert turtle.x == expected_x
    assert turtle.y == expected_y
