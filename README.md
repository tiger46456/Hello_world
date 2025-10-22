# Flask Todo List

A lightweight, full-featured todo list web application built with [Flask](https://flask.palletsprojects.com/).

## Features

- 🗂️ Organised todo list with persistent storage backed by JSON
- ✅ Create, review, update, toggle, and delete tasks
- 💡 Friendly UI with responsive layout and helpful feedback messages
- 🧱 Jinja2 templating with reusable base layout

## Requirements

- Python 3.8+
- pip (Python package manager)

All Python dependencies are listed in `requirements.txt`.

## Getting started

1. **Clone the repository** (or fetch the latest changes).
2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**:

   ```bash
   flask --app app run --debug
   ```

   Alternatively, you can start the server with:

   ```bash
   python app.py
   ```

5. Open your browser and navigate to http://127.0.0.1:5000 to access the application.

## Project structure

```
├── app.py              # Flask application entry point
├── data/
│   └── todos.json      # Simple JSON storage for todos
├── templates/
│   ├── base.html       # Shared layout
│   ├── index.html      # Main todo list view
│   └── edit.html       # Edit todo view
└── static/
    └── css/
        └── style.css   # Custom styles
```

## Development notes

- Todos are stored in `data/todos.json`. The file is created automatically if it doesn't exist.
- Flash messages are used to surface validation errors and confirmations.
- The UI adapts to smaller screens with mobile-friendly layouts.

## License

This project is provided under the MIT License. See [LICENSE](LICENSE) for details.
