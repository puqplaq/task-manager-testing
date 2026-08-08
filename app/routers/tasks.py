from fastapi import APIRouter, HTTPException

from app.database import db
from app.models import TaskCreate, TaskResponse, TaskUpdate

ERRORS = {404: "Task not found!"}

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "",
    response_model=list[TaskResponse],
    summary="Список задач",
    description="Возвращает список всех задач.",
)
def list_tasks():
    return db.get_all()


@router.post(
    "",
    response_model=TaskResponse,
    status_code=201,
    summary="Создать задачу",
    description='Создаёт новую задачу. Статус по умолчанию — "pending".',
)
def create_task(data: TaskCreate):
    return db.create(title=data.title, description=data.description)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получить задачу",
    description="Возвращает задачу по ID. 404, если задача не найдена.",
)
def get_task(task_id: int):
    task = db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=ERRORS[404])
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Обновить задачу",
    description="Частично обновляет title, description или status. 404, если не найдена.",
)
def update_task(task_id: int, data: TaskUpdate):
    task = db.update(task_id, **data.model_dump(exclude_unset=True))
    if task is None:
        raise HTTPException(status_code=404, detail=ERRORS[404])
    return task


@router.delete(
    "/{task_id}",
    status_code=204,
    summary="Удалить задачу",
    description="Удаляет задачу по ID. 404, если задача не найдена.",
)
def delete_task(task_id: int):
    if not db.delete(task_id):
        raise HTTPException(status_code=404, detail=ERRORS[404])
