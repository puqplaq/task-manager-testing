import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app=app)


class TestTaskLifeCycle:
    def test_full_task_lifecycle(self, client):
        resp = client.post(
            "/tasks",
            json={
                "title": "Write test",
                "description": "Writing unit-, integration and e2e-tests",
            },
        )
        assert resp.status_code == 201
        task = resp.json()
        task_id = task["id"]
        assert task["status"] == "pending"

        resp = client.get(f"/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Write test"

        resp = client.patch(f"/tasks/{task_id}", json={"status": "done"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "done"

        resp = client.get("/tasks")
        assert len(resp.json()) == 1

        resp = client.delete(f"/tasks/{task_id}")
        assert resp.status_code == 204

        resp = client.get(f"/tasks/{task_id}")
        assert resp.status_code == 404

    def test_create_multiple_tasks(self, client):
        for i in range(3):
            client.post("/tasks", json={"title": f"Task {i}"})

        resp = client.get("/tasks")
        assert len(resp.json()) == 3

    def test_update_nonexistent_task(self, client):
        resp = client.patch("/tasks/999", json={"status": "done"})
        assert resp.status_code == 404
        assert "detail" in resp.json()

    def test_delete_already_deleted(self, client):
        resp = client.post("/tasks", json={"title": "Delete task"})
        task_id = resp.json()["id"]

        client.delete(f"/tasks/{task_id}")
        resp = client.delete(f"/tasks/{task_id}")
        assert resp.status_code == 404
