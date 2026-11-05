# Classroom Task Tracker

A beginner-friendly web app to manage learning tasks. Built with **Python + Flask**, **HTML**, **CSS**, **JavaScript** and **JSON**.

> This is a normal programming project. It does **not** use AI or make predictions.

## What it does
- Add a task with a title, subject and priority (Low / Medium / High)
- View all tasks, or filter by **All**, **Pending** or **Completed**
- Mark a task as completed, reopen it, or delete it
- See total, pending and completed counts and a progress percentage
- Tasks are saved in `tasks.json`, so they stay after you restart the app

## How to run it

**Before you start:** install Python 3.10 or newer and VS Code. Extract the ZIP first (do not run files from inside the ZIP). Open the folder that directly contains `app.py`.

### Windows
Open VS Code -> File -> Open Folder -> pick the project folder -> Terminal -> New Terminal, then run one by one:
```
py --version
py -m pip install -r requirements.txt
py app.py
```

### macOS / Linux
```
python3 --version
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open **http://127.0.0.1:5000** in your browser.
To stop the server, click in the terminal and press **Ctrl + C**.

## Easy explanation: how the pieces fit together

Think of the app like a restaurant:

| Part | Restaurant | File |
|------|-----------|------|
| Frontend | The menu and table - what you see and click | `templates/index.html`, `static/style.css`, `static/app.js` |
| Backend | The kitchen - does the real work | `app.py` |
| Storage | The notebook where orders are written down | `tasks.json` |

**What happens when you add a task:**
1. You type a title and subject and click **Add task**.
2. `app.js` sends the data to Flask (`POST /api/tasks`).
3. `app.py` checks the data (is the title empty? is the priority valid?).
4. If it is OK, Python adds the task to the list and saves it in `tasks.json`.
5. Flask replies, and `app.js` reloads the list and updates the page.

## What each file does
- `app.py` - Flask server: loads/saves tasks, validates input, calculates statistics, defines the API routes.
- `templates/index.html` - the page structure (form, filters, task list, progress area).
- `static/style.css` - colours, layout and the responsive design.
- `static/app.js` - handles clicks, sends requests to the backend, redraws the page.
- `tasks.json` - the saved tasks (starts as an empty list `[]`).
- `requirements.txt` - tells pip to install Flask.
- `.gitignore` - tells Git which files not to upload.

## Python concepts used (and where to find them in `app.py`)
| Concept | Where |
|--------|-------|
| Variables and strings | `title`, `subject`, `priority`, `status` |
| Lists | the list of all tasks |
| Dictionaries | one task = `{"id": 1, "title": ..., ...}` |
| Sets | `ALLOWED_STATUSES`, `ALLOWED_PRIORITIES` |
| if / else | validation, and the 0% progress rule |
| for loops | `get_next_id()` and `update_task()` |
| List comprehensions | `filter_tasks()`, `calculate_stats()`, `delete_task()` |
| Functions | `load_tasks()`, `save_tasks()`, `calculate_stats()` ... |
| File handling + JSON | `load_tasks()` and `save_tasks()` |

## API routes
| Method and route | Purpose |
|------------------|---------|
| `GET /` | Show the webpage |
| `GET /api/tasks` | Return tasks and statistics |
| `GET /api/tasks?status=Pending` | Return only pending tasks |
| `POST /api/tasks` | Create a new task |
| `PATCH /api/tasks/1` | Update the status of task 1 |
| `DELETE /api/tasks/1` | Delete task 1 |

**Progress formula:** `progress = (completed_tasks / total_tasks) * 100`. If there are no tasks, it shows 0%.

## Example task record
```json
{
  "id": 1,
  "title": "Practice Python loops",
  "subject": "Python",
  "priority": "High",
  "status": "Pending"
}
```

## Testing checklist
- [ ] Homepage opens and shows the tracker
- [ ] Add a task - it appears as Pending
- [ ] Empty title or subject shows a validation message
- [ ] High priority is displayed
- [ ] Pending / Completed / All filters work
- [ ] Mark done - counts and progress update
- [ ] Reopen a completed task, then delete a task
- [ ] Refresh the browser - tasks are still there
- [ ] Stop and restart Flask - tasks are still in `tasks.json`
- [ ] Remove all tasks - progress shows 0%

## Common problems
| Problem | Fix |
|---------|-----|
| `python` is not recognised | Use `py` instead (Windows) |
| No module named flask | Run `py -m pip install -r requirements.txt` in the project folder |
| TemplateNotFound: index.html | `index.html` must be inside the `templates` folder |
| CSS or JS missing | `style.css` and `app.js` must be inside the `static` folder |
| Website does not open | Make sure `py app.py` is still running |
| Tasks do not save | Make sure `tasks.json` exists and the folder is writable |

## Uploading to GitHub
1. Create a repository named `classroom-task-tracker`.
2. Upload all files and folders, keeping the structure.
3. Commit with a message like `Add Classroom Task Tracker project`.
4. Do **not** upload `.venv`, `venv`, `env` or `__pycache__`, and never upload passwords or API keys.

GitHub stores your code; it does not run the Flask app as a public website.

## Limitations and future ideas
Runs locally only, with no user accounts, cloud database, hosting or reminders.
Ideas: login, SQLite, due dates, search, editing tasks, charts, reminders, deployment.
