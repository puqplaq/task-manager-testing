import pytest
from httpx import AsyncClient, ASGITransport


from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="https://test")


class TestCreateTask:
    @pytest.mark.asyncio
    async def test_create_returns_201(self, client):
        resp = await client.post("/tasks", json={"title": "Create task"})
        assert resp.status_code == 201
        assert resp.json()["title"] == "Create task"

    @pytest.mark.asyncio
    async def test_create_without_description(self, client):
        resp = await client.post("/tasks", json={"title": "Write test"})
        assert resp.status_code == 201
        assert resp.json()["description"] == ""

    @pytest.mark.asyncio
    async def test_create_without_title_returns_422(self, client):
        resp = await client.post("/tasks", json={})
        assert resp.status_code == 422
        

class TestGetTask:
    @pytest.mark.asyncio
    async def test_get_empty_list(self, client):
        resp = await client.get("/tasks")
        assert resp.status_code == 200
        assert resp.json() == []
        
    @pytest.mark.asyncio
    async def test_get_after_create(self, client):
        await client.post("/tasks", json={"title": "Post task"})
        resp = await client.get("/tasks")
        assert len(resp.json()) == 1
        
        
class TestGetSingleTask:
    @pytest.mark.asyncio
    async def test_get_existing(self, client):
        created = await client.post("/tasks", json={"title": "Create task"})
        task_id = created.json()["id"]
        
        resp = await client.get(f"/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == task_id
        
    @pytest.mark.asyncio
    async def test_get_nonexistent_returns_404(self, client):
        resp = await client.get("/tasks/9999")
        assert resp.status_code == 404
        

class TestUpdateTask:
    @pytest.mark.asyncio
    async def test_update_status(self, client):
        created = await client.post("/tasks", json={"title": "Update task"})
        task_id = created.json()["id"]
        
        resp = await client.patch(f"/tasks/{task_id}", json={"status": "done"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "done"
        
    @pytest.mark.asyncio
    async def test_update_nonexistent_returns_404(self, client):
        resp = await client.patch("/tasks/9999", json={"status": "done"})
        assert resp.status_code == 404
        

class TestDeleteTask:
    @pytest.mark.asyncio
    async def test_delete_returns_204(self, client):
        created = await client.post("/tasks", json={"title": "Delete task"})
        task_id = created.json()["id"]
        
        resp = await client.delete(f"/tasks/{task_id}")
        assert resp.status_code == 204
        
    @pytest.mark.asyncio
    async def test_delete_nonexistent_returns_404(self, client):
        resp = await client.delete("/tasks/9999")
        assert resp.status_code == 404
        