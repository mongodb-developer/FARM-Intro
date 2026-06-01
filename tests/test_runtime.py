import asyncio
import importlib.util
import sys
import types
import unittest
from pathlib import Path


class RuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = types.ModuleType("config")
        config.settings = types.SimpleNamespace(DB_URL="mongodb://example/test", DB_NAME="sample", HOST="127.0.0.1", DEBUG_MODE=False, PORT=8000)
        sys.modules["config"] = config

        sys.modules.setdefault("uvicorn", types.ModuleType("uvicorn"))

        pymongo = types.ModuleType("pymongo")
        class _AsyncMongoClient:
            def __init__(self, *a, **kw): self.closed = False
            def __getitem__(self, name): return {"db_name": name}
            def close(self): self.closed = True
        pymongo.AsyncMongoClient = _AsyncMongoClient
        sys.modules["pymongo"] = pymongo

        # Minimal fastapi stub with APIRouter support
        fastapi_stub = types.ModuleType("fastapi")
        class APIRouter:
            def __init__(self):
                self._routes = []
            def get(self, path, **kwargs):
                def wrap(fn):
                    self._routes.append(types.SimpleNamespace(path=path, endpoint=fn))
                    return fn
                return wrap
        class FastAPI:
            def __init__(self, *args, **kwargs):
                self._routers = []
                self.mongodb = None
                self.mongodb_client = None
            def on_event(self, event):
                return lambda fn: fn
            def include_router(self, router, *, prefix="", **kwargs):
                self._routers.append((router, prefix))
            @property
            def routes(self):
                return [
                    types.SimpleNamespace(path=prefix + r.path)
                    for router, prefix in self._routers
                    for r in router._routes
                ]
        fastapi_stub.FastAPI = FastAPI
        fastapi_stub.APIRouter = APIRouter
        sys.modules["fastapi"] = fastapi_stub

        todo_routers = types.ModuleType("apps.todo.routers")
        router = APIRouter()
        @router.get("/hello")
        async def hello():
            return {"ok": True}
        todo_routers.router = router
        sys.modules["apps.todo.routers"] = todo_routers

        target = Path(__file__).resolve().parents[1] / "backend" / "main.py"
        spec = importlib.util.spec_from_file_location("farm_intro_main", target)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_startup_and_router_mount(self):
        class FakeClient:
            def __init__(self, *args, **kwargs):
                self.closed = False
            def __getitem__(self, name):
                return {"db_name": name}
            def close(self):
                self.closed = True

        self.mod.AsyncMongoClient = FakeClient

        async def run_lifespan():
            async with self.mod.lifespan(self.mod.app):
                self.assertTrue(hasattr(self.mod.app, "mongodb"))
                paths = {route.path for route in self.mod.app.routes}
                self.assertIn("/task/hello", paths)
            self.assertTrue(self.mod.app.mongodb_client.closed)

        asyncio.run(run_lifespan())


if __name__ == "__main__":
    unittest.main()
