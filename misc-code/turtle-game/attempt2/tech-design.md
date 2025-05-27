# Overvidew
Turtle game

# Game functionality
- Single board
- Single turtle
- Turtle moves up, down, left, right on board
- Able to place obstacles on board

# Entities

## Board
- Contains single turtle

- Representation
    - 2D grid representation
        - 1 = open
        - 0 = occupied
    - Each coordinate is an open position (unless taken up by something else)

- Constructor constructs a basic NxM board

## Turtle
- Moves on a single board

- Constructor constructs a basic Turtle
    - Requires a board - simplest - you can't do anything about a Turtle without a board

## Game
[ ] Optional - can have a game entity that's like an Aggregate which encapsulates board and turtle(s)