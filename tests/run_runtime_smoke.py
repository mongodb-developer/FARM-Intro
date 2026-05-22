#!/usr/bin/env python3
"""Repo-specific runtime contract test.

This validates that the repository's primary runtime module(s):
- compile successfully
- keep expected runtime entrypoints/routes/contracts
"""

from __future__ import annotations

from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]


def require_file(path: str) -> Path:
    p = ROOT / path
    if not p.exists():
        raise AssertionError(f"Missing expected file: {path}")
    return p


def compile_file(path: str) -> None:
    p = require_file(path)
    py_compile.compile(str(p), doraise=True)


def read_text(path: str) -> str:
    return require_file(path).read_text()


def require_contains(path: str, needle: str) -> None:
    text = read_text(path)
    if needle not in text:
        raise AssertionError(f"Expected marker not found in {path}: {needle}")


def ok(msg: str) -> None:
    print(f"PASS: {msg}")


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def main() -> int:
    try:
        repo = ROOT.name

        if repo == "FARM-Auth":
            compile_file("backend/main.py")
            require_contains("backend/main.py", "app = FastAPI()")
            require_contains("backend/main.py", "@app.on_event(\"startup\")")
            require_contains("backend/main.py", "get_users_router")
            require_contains("backend/main.py", "get_todo_router")
            ok("FARM-Auth runtime contracts")

        elif repo == "FARM-Intro":
            compile_file("backend/main.py")
            require_contains("backend/main.py", "app = FastAPI()")
            require_contains("backend/main.py", "app.include_router(todo_router")
            require_contains("backend/main.py", "prefix=\"/task\"")
            ok("FARM-Intro runtime contracts")

        elif repo == "a2a-mcp-mongodb-multiagents":
            compile_file("mcp/main.py")
            require_contains("mcp/main.py", "mcp = FastMCP(")
            require_contains("mcp/main.py", "@mcp.tool")
            require_contains("mcp/main.py", "async def connect_to_mongo")
            ok("a2a MCP runtime contracts")

        elif repo == "beanie-example":
            compile_file("src/beaniecocktails/__init__.py")
            compile_file("src/beaniecocktails/scripts/init_db.py")
            require_contains("src/beaniecocktails/__init__.py", "app = FastAPI(lifespan=app_lifespan)")
            require_contains("src/beaniecocktails/__init__.py", "init_beanie(")
            require_contains("src/beaniecocktails/__init__.py", "app.include_router(cocktail_router")
            ok("beanie-example runtime contracts")

        elif repo == "docbridge":
            compile_file("examples/why/why/__init__.py")
            require_contains("examples/why/why/__init__.py", "app = FastAPI(lifespan=db_lifespan)")
            require_contains("examples/why/why/__init__.py", "@app.get(\"/profiles/{user_id}\")")
            require_contains("examples/why/why/__init__.py", "class Profile(Document)")
            ok("docbridge runtime contracts")

        elif repo == "farm-stack-to-do-app":
            compile_file("backend/src/todo/server.py")
            require_contains("backend/src/todo/server.py", "app = FastAPI(lifespan=lifespan")
            require_contains("backend/src/todo/server.py", "@app.get(\"/api/lists\")")
            require_contains("backend/src/todo/server.py", "@app.post(\"/api/lists\"")
            require_contains("backend/src/todo/server.py", "@app.patch(\"/api/lists/{list_id}/checked_state\")")
            ok("farm-stack-to-do-app runtime contracts")

        elif repo == "hr_agentic_chatbot":
            compile_file("app.py")
            require_contains("app.py", "@cl.on_chat_start")
            require_contains("app.py", "@cl.on_message")
            require_contains("app.py", "create_workflow(")
            ok("hr_agentic_chatbot runtime contracts")

        elif repo == "mongodb-atlas-fastapi":
            compile_file("app/main.py")
            require_contains("app/main.py", "app = FastAPI()")
            require_contains("app/main.py", "@app.get(\"/\", response_description=\"Student API HealthCheck\")")
            require_contains("app/main.py", "@app.get(\"/students\"")
            ok("mongodb-atlas-fastapi runtime contracts")

        elif repo == "mongodb-with-starlette":
            compile_file("app.py")
            require_contains("app.py", "app = Starlette(")
            require_contains("app.py", "Route(\"/\", create_student, methods=[\"POST\"])")
            require_contains("app.py", "Route(\"/{id}\", delete_student, methods=[\"DELETE\"])")
            ok("mongodb-with-starlette runtime contracts")

        elif repo == "mongodb-with-tornado":
            compile_file("app.py")
            require_contains("app.py", "class MainHandler(tornado.web.RequestHandler)")
            require_contains("app.py", "app = tornado.web.Application(")
            require_contains("app.py", "(r\"/(?P<student_id>\\w+)\", MainHandler)")
            ok("mongodb-with-tornado runtime contracts")

        elif repo == "mongodb-with-sanic":
            compile_file("app.py")
            require_contains("app.py", "app = Sanic(__name__)")
            require_contains("app.py", "@app.route(\"/\", methods=[\"POST\"])")
            require_contains("app.py", "@app.route(\"/<id>\", methods=[\"DELETE\"])")
            ok("mongodb-with-sanic runtime contracts")

        elif repo == "celeb-matcher-farm":
            compile_file("backend/src/server.py")
            require_contains("backend/src/server.py", "app = FastAPI(lifespan=lifespan")
            require_contains("backend/src/server.py", "@app.post(\"/api/search\")")
            require_contains("backend/src/server.py", "class SearchPayload(BaseModel)")
            ok("celeb-matcher-farm runtime contracts")

        else:
            raise AssertionError(f"No repository-specific contract defined for: {repo}")

        return 0
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    sys.exit(main())
