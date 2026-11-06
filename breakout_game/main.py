
from tkinter import TclError
from turtle import Screen, Terminator
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import Scoreboard

# Create the screen
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Breakout Game")
screen.tracer(0)

# Create game objects
paddle = Paddle()
ball = Ball()
scoreboard = Scoreboard()

# Create bricks

# Create bricks
bricks = []

brick_colors = ["red", "orange", "yellow", "green", "blue"]

for row in range(5):
    for column in range(10):

        x = -315 + column * 70
        y = 220 - row * 35

        color = brick_colors[row]

        brick = Brick((x, y), color)
        bricks.append(brick)

# Keyboard controls
screen.listen()
screen.onkey(paddle.go_right, "Right")
screen.onkey(paddle.go_left, "Left")

game_is_on = True
timer_id = None
window = screen.getcanvas().winfo_toplevel()


def close_game():
    global game_is_on, timer_id

    game_is_on = False
    if timer_id is not None:
        window.after_cancel(timer_id)
        timer_id = None
    screen.bye()


window.protocol("WM_DELETE_WINDOW", close_game)


def game_loop():
    global timer_id

    if not game_is_on:
        return

    timer_id = None
    try:
        screen.update()
    except (Terminator, TclError):
        if game_is_on:
            raise
        return

    if not game_is_on:
        return

    # Move the ball
    ball.move()

    # Detect collision with side walls
    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.bounce_x()

    # Detect collision with top wall
    if ball.ycor() > 280:
        ball.bounce_y()

    # Detect collision with paddle
    if ball.distance(paddle) < 50 and ball.y_move < 0:
        ball.bounce_y()

    # Detect when the ball falls
    if ball.ycor() < -280:
        ball.goto(0, 0)
        ball.bounce_y()

    timer_id = window.after(100, game_loop)


game_loop()
screen.mainloop()
