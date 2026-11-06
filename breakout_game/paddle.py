

from turtle import Turtle

class Paddle(Turtle):

    def __init__(self):
        """ Initializes the paddle object with a square shape, white color, and specific size. The paddle is positioned at the bottom of the screen.
        """
        super().__init__()

        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(0, -250)
    
    def go_right(self):
        """ Moves the paddle to the right by 20 units. """
        new_x = self.xcor() + 20
        self.goto(new_x, self.ycor())

    def go_left(self):
        """ Moves the paddle to the left by 20 units. """
        new_x = self.xcor() - 20
        self.goto(new_x, self.ycor())
