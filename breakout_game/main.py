
from tkinter import TclError
from turtle import Screen, Terminator
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import Scoreboard

BALL_RADIUS = 10
BRICK_HALF_WIDTH = 30
BRICK_HALF_HEIGHT = 10
PADDLE_HALF_WIDTH = 50
PADDLE_HALF_HEIGHT = 10

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


def check_brick_collisions():
    for brick in bricks[:]:
        overlap_x = BALL_RADIUS + BRICK_HALF_WIDTH - abs(ball.xcor() - brick.xcor())
        overlap_y = BALL_RADIUS + BRICK_HALF_HEIGHT - abs(ball.ycor() - brick.ycor())

        if overlap_x > 0 and overlap_y > 0:
            brick.hideturtle()
            bricks.remove(brick)
            scoreboard.increase_score()

            if overlap_x < overlap_y:
                ball.bounce_x()
            else:
                ball.bounce_y()
            return


def check_paddle_collision(previous_y):
    paddle_top = paddle.ycor() + PADDLE_HALF_HEIGHT
    ball_bottom = ball.ycor() - BALL_RADIUS
    hit_paddle = (
        ball.y_move < 0
        and previous_y - BALL_RADIUS >= paddle_top
        and ball_bottom <= paddle_top
        and abs(ball.xcor() - paddle.xcor()) <= PADDLE_HALF_WIDTH + BALL_RADIUS
    )

    if hit_paddle:
        ball.sety(paddle_top + BALL_RADIUS)
        ball.bounce_y()


def game_loop():
    global game_is_on, timer_id

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
    previous_y = ball.ycor()
    ball.move()

    # Detect collision with side walls
    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.bounce_x()

    # Detect collision with top wall
    if ball.ycor() > 280:
        ball.bounce_y()

    # Remove hit bricks and award points
    check_brick_collisions()

    # Bounce the ball upward when it hits the paddle
    check_paddle_collision(previous_y)

    # End the game when the ball passes below the paddle
    if ball.ycor() < paddle.ycor() - PADDLE_HALF_HEIGHT - BALL_RADIUS:
        game_is_on = False
        scoreboard.game_over()
        screen.update()
        return

    timer_id = window.after(100, game_loop)


game_loop()
screen.mainloop()
