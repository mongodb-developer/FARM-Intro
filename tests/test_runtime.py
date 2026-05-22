import asyncio
import importlib.util
import sys
import types
import unittest
from pathlib import Path

from fastapi import APIRouter


class RuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = types.ModuleType("config")
        config.settings = types.SimpleNamespace(DB_URL="mongodb://example/test", DB_NAME="sample", HOST="127.0.0.1", DEBUG_MODE=False, PORT=8000)
        sys.modules["config"] = config

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

        class FakeClient:
            def __init__(self, *args, **kwargs):
                self.closed = False
            def __getitem__(self, name):
                return {"db_name": name}
            def close(self):
                self.closed = True

        cls.mod.AsyncMongoClient = FakeClient

    def test_startup_and_router_mount(self):
        asyncio.run(self.mod.startup_db_client())
        self.assertTrue(hasattr(self.mod.app, "mongodb"))
        paths = {route.path for route in self.mod.app.routes}
        self.assertIn("/task/hello", paths)
        asyncio.run(self.mod.shutdown_db_client())
        self.assertTrue(self.mod.app.mongodb_client.closed)


if __name__ == "__main__":
    unittest.main()
