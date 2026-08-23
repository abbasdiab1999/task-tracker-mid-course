from __future__ import annotations

from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .models import (
    TaskCreate, TaskUpdate, TaskResponse,
    TaskStatus, TaskPriority
)
from . import storage
from .business_rules import validate_status_transition, is_overdue

app = FastAPI(title="Task Tracker - Mid-Course Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serialize(task: dict) -> TaskResponse:
    return TaskResponse(**task, overdue=is_overdue(task))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate):
    return serialize(storage.add_task(payload))


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
    tag: Optional[str] = Query(default=None, min_length=1),
):
    tasks = storage.list_tasks()
    if status is not None:
        tasks = [t for t in tasks if t["status"] == status]
    if priority is not None:
        tasks = [t for t in tasks if t["priority"] == priority]
    if overdue is not None:
        tasks = [t for t in tasks if is_overdue(t) is overdue]
    if tag:
        needle = tag.strip().lower()
        tasks = [t for t in tasks if any(x.lower() == needle for x in t.get("tags", []))]
    return [serialize(t) for t in tasks]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = storage.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return serialize(task)


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(task_id: int, payload: TaskUpdate):
    current = storage.get_task(task_id)
    if not current:
        raise HTTPException(status_code=404, detail="Task not found")

    changes = payload.model_dump(exclude_unset=True)
    if "status" in changes:
        try:
            validate_status_transition(current["status"], changes["status"])
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    updated = storage.update_task(task_id, changes)
    return serialize(updated)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")


# Optional built-in frontend for easy demo.
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def frontend():
    return FileResponse("frontend/index.html")
