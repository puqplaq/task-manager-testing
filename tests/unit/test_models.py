import pytest
from pydantic import ValidationError


from app.models import TaskCreate, TaskUpdate, TaskResponse


class TestTaskCreate:
    def test_valid_task(self):
        task = TaskCreate(title="Create task")
        assert task.title == "Create task"
        assert task.description == ""

    def test_with_description(self):
        task = TaskCreate(title="Create task", description="Creating task")
        assert task.description == "Creating task"

    def test_title_required(self):
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate()
        assert "title" in str(exc_info.value)

    def test_title_cannot_be_empty(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="")


class TestTaskUpdate:
    def test_partial_update(self):
        update = TaskUpdate(status="done")
        assert update.status == "done"
        assert update.title is None

    def test_all_fields_optional(self):
        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.status is None


class TestTaskResponse:
    def test_from_database_task(self):
        task = TaskResponse(id=1, title="Test", description="", status="pending")
        assert task.id == 1
        assert task.title == "Test"
        assert task.description == ""
        assert task.status == "pending"
