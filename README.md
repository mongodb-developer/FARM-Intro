# FARM Stack To-Do App

A full-stack task manager built with **FastAPI**, **React**, and **MongoDB** — the FARM stack. Demonstrates async CRUD operations from a React frontend through a FastAPI backend to a MongoDB collection, with all three tiers running locally via Docker Compose.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/mongodb-developer/FARM-Intro)

---

## Features

- Create, read, update, and delete to-do tasks
- Async FastAPI backend with `AsyncMongoClient` (pymongo 4.x)
- React 18 frontend with Ant Design 5 timeline UI
- Auto-refreshing task list (polling every second)
- Seed-free: tasks persist in MongoDB across restarts
- Swagger UI at `/docs` for interactive API exploration

## Tech Stack

| Layer    | Technology                        | Version |
|----------|-----------------------------------|---------|
| Backend  | FastAPI + uvicorn                 | 0.136+  |
| Database | MongoDB (pymongo AsyncMongoClient)| 4.17+   |
| Frontend | React + Ant Design                | 18 / 5  |
| Runtime  | Python                            | 3.13    |
| Node     | Node.js                           | 22      |

## Architecture Overview

```
Browser (React 18 + antd 5)
        │  fetch /task/
        ▼
FastAPI (uvicorn, port 8000)
  └─ /task  →  apps/todo/routers.py  →  AsyncMongoClient
                                               │
                                        MongoDB :27017
                                        database: farm_intro
                                        collection: tasks
```

## Prerequisites

- Python 3.13+
- Node.js 22+
- Docker 24+ (for local MongoDB)
- MongoDB Atlas cluster **or** local Docker MongoDB

## Quick Start

```bash
# 1. Clone
git clone https://github.com/mongodb-developer/FARM-Intro
cd FARM-Intro

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
DB_URL="mongodb://localhost:27017/" DB_NAME="farm_intro" uvicorn main:app --reload
# API ready at http://localhost:8000  •  Swagger UI at http://localhost:8000/docs

# 3. Frontend (new terminal)
cd ../frontend
npm install
REACT_APP_BACKEND_URL=http://localhost:8000 npm start
# UI ready at http://localhost:3000
```

## Run in Codespaces / Dev Container

Click **Open in GitHub Codespaces** above — MongoDB Atlas Local starts automatically and the backend seed runs on container start. No local install required.

## Environment Variables

| Variable  | Required | Example                          | Description                     |
|-----------|----------|----------------------------------|---------------------------------|
| `DB_URL`  | Yes      | `mongodb://localhost:27017/`     | MongoDB connection string        |
| `DB_NAME` | Yes      | `farm_intro`                     | Target database name             |
| `HOST`    | No       | `0.0.0.0`                        | uvicorn bind address (default)   |
| `PORT`    | No       | `8000`                           | uvicorn port (default)           |
| `DEBUG_MODE` | No    | `false`                          | Enable uvicorn auto-reload       |

## API Overview

| Method | Path         | Description          |
|--------|--------------|----------------------|
| GET    | `/task/`     | List all tasks       |
| POST   | `/task/`     | Create a task        |
| GET    | `/task/{id}` | Get a single task    |
| PUT    | `/task/{id}` | Update a task        |
| DELETE | `/task/{id}` | Delete a task        |

Full interactive docs: `http://localhost:8000/docs`

## Project Structure

```
FARM-Intro/
├── backend/
│   ├── main.py                  # FastAPI app + lifespan (DB connect/close)
│   ├── config/                  # pydantic-settings config
│   ├── apps/todo/
│   │   ├── models.py            # TaskModel, UpdateTaskModel (pydantic v2)
│   │   └── routers.py           # CRUD route handlers
│   ├── requirements.in          # Direct dependencies
│   └── requirements.txt         # Pinned lockfile (Python 3.13)
├── frontend/
│   └── src/App.js               # React 18 task timeline
├── tests/
│   ├── test_runtime.py          # Offline unit test (mocked pymongo)
│   └── test_integration.py      # Live MongoDB CRUD tests
└── .github/workflows/ci.yml
```

## Testing

```bash
# Runtime (no MongoDB needed)
python tests/test_runtime.py

# Integration (requires MongoDB)
MONGODB_URI="mongodb://localhost:27017/" pytest tests/test_integration.py -v
```

CI runs both test suites on every push using a `mongo:latest` service container — no Atlas secrets needed.

## Why MongoDB?

- [AsyncMongoClient](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/async/) — native async support for FastAPI/asyncio apps
- [Flexible document model](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/) — no migration needed as task fields evolve
- [MongoDB Atlas](https://www.mongodb.com/atlas) — managed cloud option that requires only a `DB_URL` change

## Additional Resources

- Blog post: [FARM Stack Introduction](https://www.mongodb.com/developer/languages/python/farm-stack-fastapi-react-mongodb/)
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [pymongo async docs](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/async/)

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ValidationError: DB_URL field required` | Set `DB_URL` and `DB_NAME` env vars before starting uvicorn |
| `ServerSelectionTimeoutError` | Check that MongoDB is running and `DB_URL` points to it |
| `ModuleNotFoundError: pydantic_settings` | Run `pip install -r requirements.txt` (needs `pydantic-settings`) |
| React `npm start` fails on Node 18 | Use Node 22: `nvm use 22` |
| Frontend shows empty timeline | Backend not running or CORS issue; confirm `http://localhost:8000/task/` returns JSON |

