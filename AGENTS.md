# AGENTS.md — FARM Stack To-Do App

Agent guide for AI coding assistants working in this repository.

## Build and Test Commands

```bash
# Backend — install and start
cd backend
pip install -r requirements.txt
DB_URL="mongodb://localhost:27017/" DB_NAME="farm_intro" uvicorn main:app --reload

# Frontend — install and start
cd frontend
npm install
npm start

# Tests (no MongoDB needed)
python tests/test_runtime.py

# Integration tests (MongoDB required)
MONGODB_URI="mongodb://localhost:27017/" pytest tests/test_integration.py -v

# Regenerate backend lockfile
cd backend && pip-compile --upgrade requirements.in
```

## Project Structure

```
FARM-Intro/
├── backend/
│   ├── main.py                  # FastAPI app, lifespan (DB connect/close), appName
│   ├── config/__init__.py       # pydantic-settings: DB_URL, DB_NAME, HOST, PORT
│   ├── apps/todo/
│   │   ├── models.py            # TaskModel and UpdateTaskModel (pydantic v2)
│   │   └── routers.py           # CRUD handlers for /task/ prefix
│   ├── requirements.in          # Direct dependencies (source of truth)
│   └── requirements.txt         # Pinned lockfile — regenerate with pip-compile
├── frontend/
│   ├── src/App.js               # React 18 task list; polls /task/ every 1 s
│   └── package.json             # React 18, antd 5, react-scripts 5
├── tests/
│   ├── test_runtime.py          # Offline unit test; stubs FastAPI and pymongo
│   └── test_integration.py      # Live CRUD tests against MongoDB
├── .github/workflows/ci.yml     # CI: Python 3.13, Node 22, mongo:latest service
├── .devcontainer/               # Codespaces/Dev Container with Atlas Local
├── EDD.md                       # MongoDB data model specification
└── README.md
```

## Environment Variables

| Variable    | Required | Default  | Description                       |
|-------------|----------|----------|-----------------------------------|
| `DB_URL`    | Yes      | —        | MongoDB connection string          |
| `DB_NAME`   | Yes      | —        | Database name                     |
| `HOST`      | No       | `0.0.0.0`| uvicorn bind address              |
| `PORT`      | No       | `8000`   | uvicorn port                      |
| `DEBUG_MODE`| No       | `false`  | Enable uvicorn auto-reload        |

## Key Conventions

- **Pydantic v2**: use `model_config = ConfigDict(...)` and `json_schema_extra`; never `class Config`
- **Lifespan**: DB init/teardown lives in the `@asynccontextmanager lifespan(app)` function in `main.py`; never use `@app.on_event`
- **appName**: the pymongo client is always created with `appName="farm-intro-api"`
- **No seed script**: tasks are created by users; the integration tests create and clean up their own data
- **Collection name**: `tasks` in the database specified by `DB_NAME`
- **Task `_id`**: UUID string (not ObjectId) — see EDD.md

## When To Use EDD.md

Use [EDD.md](./EDD.md) as the source of truth for the MongoDB data model in this repository.

Consult [EDD.md](./EDD.md) before making changes that touch:

- MongoDB collections, document structure, or field names
- FastAPI routes that read or write database records
- Validation, form fields, API payloads, or UI that depend on persisted data
- Schema documentation, Mermaid diagrams, or entity modelling discussions

## MongoDB Skills

Use the official MongoDB agent skills from https://github.com/mongodb/agent-skills
whenever the task is MongoDB-specific and a matching skill exists.
