import random

from locust import HttpUser, between, events, task


class TaskAPIUser(HttpUser):
    wait_time = between(1, 3)
    task_ids = []

    def on_start(self):
        for i in range(5):
            response = self.client.post(
                "/tasks",
                json={
                    "title": f"Task {random.randint(1000, 9999)}",
                    "description": f"Description for task {i}",
                },
            )
            if response.status_code == 201:
                task_id = response.json().get("id")
                if task_id:
                    self.task_ids.append(task_id)

    @task(3)
    def list_tasks(self):
        self.client.get("/tasks")

    @task(2)
    def get_task(self):
        if self.task_ids:
            task_id = random.choice(self.task_ids)
            self.client.get(f"/tasks/{task_id}")

    @task(1)
    def create_task(self):
        self.client.post(
            "/tasks",
            json={
                "title": f"New Task {random.randint(1000, 9999)}",
                "description": "Auto-generated task description",
            },
        )

    @task(1)
    def update_task(self):
        if self.task_ids:
            task_id = random.choice(self.task_ids)
            updates = []
            if random.random() > 0.5:
                updates.append({"title": f"Updated {random.randint(1000, 9999)}"})
            if random.random() > 0.5:
                updates.append({"status": random.choice(["in_progress", "completed"])})
            if updates:
                payload = {}
                for update in updates:
                    payload.update(update)
                self.client.patch(f"/tasks/{task_id}", json=payload)

    @task(1)
    def delete_task(self):
        if self.task_ids:
            task_id = self.task_ids.pop()
            self.client.delete(f"/tasks/{task_id}")


class HeavyLoadUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(5)
    def rapid_list_tasks(self):
        self.client.get("/tasks")

    @task(3)
    def rapid_create_tasks(self):
        self.client.post(
            "/tasks",
            json={
                "title": f"Stress Test {random.randint(10000, 99999)}",
                "description": "Stress test task",
            },
        )


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("=" * 50)
    print("Starting load test for Task Manager API")
    print(f"Target host: {environment.host}")
    print("=" * 50)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("=" * 50)
    print("Load test completed!")
    stats = environment.runner.stats
    print(f"Total requests: {stats.total.num_requests}")
    print(f"Total failures: {stats.total.failures}")
    print(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    print(f"99th percentile: {stats.total.get_response_time_percentile(0.99):.2f}ms")
    print("=" * 50)
