
from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import Scoreboard
import time

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
bricks = []

for row in range(3):
    for column in range(10):
        x = -315 + column * 70
        y = 200 - row * 35

        brick = Brick((x, y))
        bricks.append(brick)

# Keyboard controls
screen.listen()
screen.onkey(paddle.go_right, "Right")
screen.onkey(paddle.go_left, "Left")

# Main game loop
game_is_on = True

while game_is_on:
    time.sleep(0.1)
    screen.update()

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

screen.exitonclick()
