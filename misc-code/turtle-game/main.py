"""
Executes the turtle game.
"""
import assets


# TODO: think about where to put translate_dir
def translate_dir(input_str: str) -> str:
    if input_str == '\x1b[A':
        return 'up'
    elif input_str == '\x1b[B':
        return 'down'
    elif input_str == '\x1b[C':
        return 'right'
    elif input_str == '\x1b[D':
        return 'left'
    return ''


def main():
    """
    Funcitonal requirements:
    - Start the turtle at a coordinate (x,y) on a board
    - Input arrow keys to move the turtle
    - Place obstacles on the board (positions) at beginning of game

    Components:
    - Need a board to move the turtle on.
    - Need a turtle interface to move (probaby a class instance)
    """

    board = assets.Board(10, 10)
    turtle = assets.Turtle(0, 0, board)

    # Listen for arrow key events from keyboard and attempt to move turtle on
    # board
    # TODO: Practice mocking out input
    while True:
        direction = translate_dir(input("Press arrow key and hit enter: "))
        turtle.move(direction)
        print(turtle)


if __name__ == "__main__":
    main()