"""Integration tests for FARM-Intro.

Tests real MongoDB CRUD operations for the task data model
used by the FARM-Intro backend.

Requires a running MongoDB instance. Set MONGODB_URI (default:
mongodb://admin:mongodb@localhost:27017/) or the tests will be skipped.
"""

import os
import pytest
from pymongo import MongoClient
from bson import ObjectId

MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://admin:mongodb@localhost:27017/")
TEST_DB = "farm_intro_integration_test"


@pytest.fixture(scope="module")
def db():
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    try:
        client.admin.command("ping")
    except Exception:
        client.close()
        pytest.skip(f"MongoDB not reachable at {MONGODB_URI}")
    database = client[TEST_DB]
    yield database
    client.drop_database(TEST_DB)
    client.close()


def test_mongodb_ping():
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    try:
        result = client.admin.command("ping")
        assert result.get("ok") == 1.0
    except Exception:
        pytest.skip(f"MongoDB not reachable at {MONGODB_URI}")
    finally:
        client.close()


def test_task_create_and_find(db):
    """Tasks collection: insert and retrieve a task."""
    tasks = db["tasks"]

    task_id = str(ObjectId())
    task = {
        "_id": task_id,
        "title": "Learn FastAPI",
        "description": "Build a FARM stack app",
        "completed": False,
    }

    result = tasks.insert_one(task)
    assert result.inserted_id == task_id

    found = tasks.find_one({"_id": task_id})
    assert found["title"] == "Learn FastAPI"
    assert found["completed"] is False

    # Cleanup
    tasks.delete_one({"_id": task_id})


def test_task_update(db):
    """Tasks collection: update a task's completion status."""
    tasks = db["tasks"]

    task_id = str(ObjectId())
    tasks.insert_one({"_id": task_id, "title": "Write tests", "completed": False})

    tasks.update_one({"_id": task_id}, {"$set": {"completed": True}})
    updated = tasks.find_one({"_id": task_id})
    assert updated["completed"] is True

    # Cleanup
    tasks.delete_one({"_id": task_id})


def test_task_list(db):
    """Tasks collection: list all tasks returns correct count."""
    tasks = db["tasks"]

    ids = [str(ObjectId()) for _ in range(3)]
    docs = [
        {"_id": ids[0], "title": "Task 1", "completed": False},
        {"_id": ids[1], "title": "Task 2", "completed": True},
        {"_id": ids[2], "title": "Task 3", "completed": False},
    ]
    tasks.insert_many(docs)

    all_tasks = list(tasks.find({}))
    assert len(all_tasks) >= 3

    incomplete = list(tasks.find({"completed": False}))
    assert all(not t["completed"] for t in incomplete)

    # Cleanup
    tasks.delete_many({"_id": {"$in": ids}})


def test_task_delete(db):
    """Tasks collection: delete a task and confirm it is gone."""
    tasks = db["tasks"]

    task_id = str(ObjectId())
    tasks.insert_one({"_id": task_id, "title": "To be deleted", "completed": False})

    delete_result = tasks.delete_one({"_id": task_id})
    assert delete_result.deleted_count == 1

    assert tasks.find_one({"_id": task_id}) is None


def test_task_not_found(db):
    """Tasks collection: querying a non-existent task returns None."""
    tasks = db["tasks"]
    assert tasks.find_one({"_id": "nonexistent-id"}) is None
