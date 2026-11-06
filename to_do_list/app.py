from flask import Flask, flash, redirect, render_template, request, url_for

from models import Task, db

# Initialize Flask app and configure database
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-key-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

with app.app_context():
    db.create_all()

# Define routes for the to-do list application
@app.get("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    edit_task_id = request.args.get("edit", type=int)
    edit_task = db.session.get(Task, edit_task_id) if edit_task_id else None
    return render_template("index.html", tasks=tasks, edit_task=edit_task)


@app.post("/add")
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Écris une tâche avant de l’ajouter.", "error")
        return redirect(url_for("index"))

    db.session.add(Task(title=title))
    db.session.commit()
    flash("Tâche ajoutée.", "success")
    return redirect(url_for("index"))


@app.post("/<int:task_id>/toggle")
def toggle_task(task_id):
    task = db.get_or_404(Task, task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.post("/<int:task_id>/edit")
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    title = request.form.get("title", "").strip()
    if not title:
        flash("Le titre ne peut pas être vide.", "error")
        return redirect(url_for("index", edit=task.id))

    task.title = title
    db.session.commit()
    flash("Tâche modifiée.", "success")
    return redirect(url_for("index"))


@app.post("/<int:task_id>/delete")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Tâche supprimée.", "success")
    return redirect(url_for("index"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
