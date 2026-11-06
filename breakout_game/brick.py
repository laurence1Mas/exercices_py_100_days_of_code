
from turtle import Turtle


class Brick(Turtle):
    def __init__(self, position):
        super().__init__()

        self.shape("square")
        self.color("orange")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.penup()
        self.goto(position)
