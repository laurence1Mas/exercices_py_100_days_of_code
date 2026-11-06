from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the Task model for the to-do list application
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
