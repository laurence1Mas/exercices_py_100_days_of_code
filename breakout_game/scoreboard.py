
from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()

        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-350, 260)

        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(
            f"Score: {self.score}",
            align="left",
            font=("Arial", 16, "normal")
        )

    def increase_score(self):
        self.score += 10
        self.update_scoreboard()
