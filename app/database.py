from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "pending"


class InMemoryDB:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def get(self, id: int) -> Task | None:
        task = self._tasks.get(id)

        if task is None:
            return None

        return task

    def create(self, title: str, description: str = "") -> Task:
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def update(self, id: int, **kwargs) -> Task | None:
        task = self._tasks.get(id)

        if task is None:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(task, key, value)

        return task

    def delete(self, id: int) -> bool:
        return self._tasks.pop(id, None) is not None

    def clear(self) -> None:
        self._tasks.clear()
        self._next_id = 1


db = InMemoryDB()
