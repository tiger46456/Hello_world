import json
import os
from typing import List, Optional

from flask import Flask, abort, flash, has_request_context, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "todos.json")


def load_todos() -> List[dict]:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as data_file:
            todos = json.load(data_file)
    except json.JSONDecodeError:
        if has_request_context():
            flash("Could not read todo data. Starting with an empty list.", "error")
        app.logger.warning("Failed to parse todo data, returning empty list", exc_info=True)
        return []

    if not isinstance(todos, list):
        return []

    normalised = []
    for todo in todos:
        if isinstance(todo, dict):
            normalised.append(
                {
                    "id": int(todo.get("id", 0)),
                    "title": str(todo.get("title", "")),
                    "description": str(todo.get("description", "")),
                    "completed": bool(todo.get("completed", False)),
                }
            )

    return normalised


def save_todos(todos: List[dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as data_file:
        json.dump(todos, data_file, indent=2, ensure_ascii=False)


def get_next_id(todos: List[dict]) -> int:
    return max((todo["id"] for todo in todos), default=0) + 1


def find_todo(todos: List[dict], todo_id: int) -> Optional[dict]:
    return next((todo for todo in todos if todo["id"] == todo_id), None)


@app.route("/")
def index():
    todos = load_todos()
    todos.sort(key=lambda todo: (todo.get("completed", False), todo.get("title", "").lower()))
    return render_template("index.html", todos=todos)


@app.post("/todos")
def create_todo():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("A title is required to create a todo.", "error")
        return redirect(url_for("index"))

    todos = load_todos()
    new_todo = {
        "id": get_next_id(todos),
        "title": title,
        "description": description,
        "completed": False,
    }

    todos.append(new_todo)
    save_todos(todos)
    flash("Todo created successfully.", "success")
    return redirect(url_for("index"))


@app.route("/todos/<int:todo_id>/edit")
def edit_todo(todo_id: int):
    todos = load_todos()
    todo = find_todo(todos, todo_id)
    if todo is None:
        abort(404)
    return render_template("edit.html", todo=todo)


@app.post("/todos/<int:todo_id>/update")
def update_todo(todo_id: int):
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    completed = request.form.get("completed") == "on"

    if not title:
        flash("A title is required to update a todo.", "error")
        return redirect(url_for("edit_todo", todo_id=todo_id))

    todos = load_todos()
    todo = find_todo(todos, todo_id)
    if todo is None:
        abort(404)

    todo.update({"title": title, "description": description, "completed": completed})
    save_todos(todos)
    flash("Todo updated successfully.", "success")
    return redirect(url_for("index"))


@app.post("/todos/<int:todo_id>/toggle")
def toggle_todo(todo_id: int):
    todos = load_todos()
    todo = find_todo(todos, todo_id)
    if todo is None:
        abort(404)

    todo["completed"] = not todo.get("completed", False)
    save_todos(todos)
    status = "completed" if todo["completed"] else "marked as pending"
    flash(f"Todo '{todo['title']}' {status}.", "info")
    return redirect(url_for("index"))


@app.post("/todos/<int:todo_id>/delete")
def delete_todo(todo_id: int):
    todos = load_todos()
    todo = find_todo(todos, todo_id)
    if todo is None:
        abort(404)

    todos = [existing for existing in todos if existing["id"] != todo_id]
    save_todos(todos)
    flash("Todo deleted successfully.", "success")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
