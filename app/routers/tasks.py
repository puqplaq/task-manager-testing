from fastapi import APIRouter, HTTPException
from models import TaskCreate, TaskUpdate, TaskResponse

from app.database import db


ERRORS = {
    404: "Task not found!"
}

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks():
    return db.get_all()


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate):
    return db.create(title=data.title, description=data.description)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=ERRORS[404])
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate):
    task = db.update(task_id, **data.model_dump(exclude_unset=True))
    if task is None:
        raise HTTPException(status_code=404, detail=ERRORS[404])
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not db.delete(task_id):
        raise HTTPException(status_code=404, detail=ERRORS[404])
