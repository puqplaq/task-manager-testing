import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def task(client):
    resp = client.post(
        "/tasks", json={"title": "Post task", "description": "Posting task"}
    )
    return resp.json()


class TestTaskResponseContract:
    def test_response_has_required_fields(self, task):
        required = {"id", "title", "description", "status"}
        assert set(task.keys()) == required

    def test_id_is_integer(self, task):
        assert isinstance(task["id"], int)

    def test_title_is_string(self, task):
        assert isinstance(task["title"], str)

    def test_description_is_string(self, task):
        assert isinstance(task["description"], str)

    def test_status_is_string(self, task):
        assert isinstance(task["status"], str)

    def test_no_extra_fields(self, task):
        allowed = {"id", "title", "description", "status"}
        assert set(task.keys()).issubset(allowed)

    def test_status_default_value(self, task):
        assert task["status"] == "pending"


class TestErrorContract:
    def test_404_response_structure(self, client):
        resp = client.get("/tasks/999")
        body = resp.json()
        assert "detail" in body
        assert isinstance(body["detail"], str)

    def test_422_response_structure(self, client):
        resp = client.post("/tasks", json={})
        body = resp.json()
        assert "detail" in body
        assert isinstance(body["detail"], list)
