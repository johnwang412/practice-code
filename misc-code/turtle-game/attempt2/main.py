"""
Engine for running turtle game
"""
from turtle_game_bo import Board, Turtle, Direction


def main():
    board = Board(10, 10)
    turtle = Turtle(0, 0, board)

    print("Initial board configuration:")
    print(board.get_string([turtle.get_position()]))

    while True:
        direction_input = input("Enter direction (w/a/s/d for up/left/down/right): ").strip().lower()

        if direction_input == 'w':
            direction = Direction.UP
        elif direction_input == 'a':
            direction = Direction.LEFT
        elif direction_input == 's':
            direction = Direction.DOWN
        elif direction_input == 'd':
            direction = Direction.RIGHT
        else:
            print("Invalid input. Please press w/a/s/d.")
            continue

        if turtle.move(direction):
            print("Turtle moved successfully.")
        else:
            print("Turtle cannot move in that direction.")

        print(board.get_string([turtle.get_position()]))

if __name__ == "__main__":
    main()
