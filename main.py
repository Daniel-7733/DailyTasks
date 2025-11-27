from flask import Flask, render_template, request, flash, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from time import gmtime, strftime
from os import path, makedirs



app: Flask = Flask(__name__)
db: SQLAlchemy = SQLAlchemy()


app.config["SECRET_KEY"] = "dev-secret"

makedirs(app.instance_path, exist_ok=True)
db_path: str = path.join(app.instance_path, "todo.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class TodoList(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    link: str = db.Column(db.String(500), nullable=True)
    note: str = db.Column(db.String(200), nullable=True)


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def home() -> str:
    """
    Home Page

    :return: home page
    """
    full_date: str = strftime("%A, %d %B %Y", gmtime())
    current_day: str = strftime("%A", gmtime())
    tasks: list[TodoList] = TodoList.query.all()
    return render_template("index.html", tasks=tasks, full_date=full_date, current_day=current_day)


@app.route("/add-task", methods=["POST"])
def add() -> Response:
    """
    This function will add task to the database

    :return: Home page
    """
    name: str = request.form["daily-task-input"]
    link: str = request.form["link-input"]
    note: str = request.form["note-text"]

    todo_list: TodoList = TodoList(name=name, link=link, note=note)
    db.session.add(todo_list)
    db.session.commit()
    flash("Task successfully added.", "success")
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id: int) -> Response:
    """
    This function will delete task to the database

    :param task_id: It will be task id which is taken from the TodoList
    :return: Home page
    """
    task: TodoList | None = TodoList.query.filter_by(id=task_id).first()

    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
