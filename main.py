from flask import Flask, render_template, request, flash, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
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
    link: str = db.Column(db.String(1000), nullable=True)
    note: str = db.Column(db.String(1000), nullable=True)


# --- DB init ---
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def home() -> str:
    """Open the home page"""
    return render_template("index.html")


@app.route("/add-task", methods=["GET", "POST"])
def add() -> str:
    """Add the task"""
    # TODO: receive data from html
    # TODO: Add data in database
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
