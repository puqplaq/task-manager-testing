from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: str


class TaskUpdate(BaseModel):
    title: str | None
    description: str | None
    status: str | None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
