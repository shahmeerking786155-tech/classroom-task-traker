"""
Classroom Task Tracker - Backend (Flask)
----------------------------------------
This file is the "brain" of the project. It:
  1. Sends the webpage to the browser.
  2. Reads and saves tasks in tasks.json.
  3. Checks user input (validation).
  4. Calculates statistics (total, pending, completed, progress %).

No AI is used here - only normal Python logic.
"""

import json
import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Build the path to tasks.json so it works no matter where you run the app from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")

# SETS: the only values we accept.
ALLOWED_STATUSES = {"Pending", "Completed"}
ALLOWED_PRIORITIES = {"Low", "Medium", "High"}


# ---------------------------------------------------------------
# FILE HANDLING FUNCTIONS (read / write tasks.json)
# ---------------------------------------------------------------
def load_tasks():
    """Read tasks.json and return a LIST of task DICTIONARIES."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        # If the file is empty or damaged, start with an empty list.
        return []
    return data if isinstance(data, list) else []


def save_tasks(tasks):
    """Write the list of tasks into tasks.json."""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


# ---------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------
def get_next_id(tasks):
    """Use a FOR LOOP to find the biggest ID, then add 1."""
    highest = 0
    for task in tasks:
        if task["id"] > highest:
            highest = task["id"]
    return highest + 1


def calculate_stats(tasks):
    """Count tasks and calculate the progress percentage."""
    total = len(tasks)
    completed = len([t for t in tasks if t["status"] == "Completed"])  # list comprehension
    pending = total - completed

    # IF/ELSE: avoid dividing by zero when there are no tasks.
    if total == 0:
        progress = 0
    else:
        progress = round((completed / total) * 100)

    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "progress": progress,
    }


def filter_tasks(tasks, status):
    """Return only tasks with the chosen status (or all of them)."""
    if status in ALLOWED_STATUSES:
        return [t for t in tasks if t["status"] == status]  # list comprehension
    return tasks


def clean_text(value):
    """Turn a value into a trimmed string (safe even if it is None)."""
    return str(value or "").strip()


# ---------------------------------------------------------------
# ROUTES (the API)
# ---------------------------------------------------------------
@app.route("/")
def home():
    """GET / -> show the webpage."""
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """GET /api/tasks?status=Pending -> return tasks + statistics."""
    tasks = load_tasks()
    status = request.args.get("status", "All")
    return jsonify({
        "tasks": filter_tasks(tasks, status),
        "stats": calculate_stats(tasks),  # stats always use ALL tasks
    })


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """POST /api/tasks -> add a new task."""
    data = request.get_json(silent=True) or {}
    title = clean_text(data.get("title"))
    subject = clean_text(data.get("subject"))
    priority = clean_text(data.get("priority")) or "Medium"

    # VALIDATION with if statements
    if not title:
        return jsonify({"error": "Please enter a task title."}), 400
    if not subject:
        return jsonify({"error": "Please enter a subject."}), 400
    if priority not in ALLOWED_PRIORITIES:
        return jsonify({"error": "Priority must be Low, Medium or High."}), 400
    if len(title) > 100 or len(subject) > 50:
        return jsonify({"error": "Title or subject is too long."}), 400

    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "subject": subject,
        "priority": priority,
        "status": "Pending",  # every new task starts as Pending
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    """PATCH /api/tasks/1 -> change the status of task 1."""
    data = request.get_json(silent=True) or {}
    status = clean_text(data.get("status"))

    if status not in ALLOWED_STATUSES:
        return jsonify({"error": "Status must be Pending or Completed."}), 400

    tasks = load_tasks()
    for task in tasks:  # FOR LOOP to search for the task
        if task["id"] == task_id:
            task["status"] = status
            save_tasks(tasks)
            return jsonify(task)

    return jsonify({"error": "Task not found."}), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """DELETE /api/tasks/1 -> remove task 1."""
    tasks = load_tasks()
    remaining = [t for t in tasks if t["id"] != task_id]  # list WITHOUT that task

    if len(remaining) == len(tasks):
        return jsonify({"error": "Task not found."}), 404

    save_tasks(remaining)
    return jsonify({"message": "Task deleted."})


if __name__ == "__main__":
    app.run(debug=True)
