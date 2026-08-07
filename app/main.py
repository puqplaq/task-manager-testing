from fastapi import FastAPI

from app.routers import tasks

app = FastAPI(title="Task Manager")
app.include_router(tasks.router)
