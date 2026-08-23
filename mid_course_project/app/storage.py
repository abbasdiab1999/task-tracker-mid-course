from __future__ import annotations

from typing import Dict
from .models import TaskCreate

_tasks: Dict[int, dict] = {}
_next_id = 1


def reset_storage() -> None:
    global _tasks, _next_id
    _tasks = {}
    _next_id = 1


def add_task(payload: TaskCreate) -> dict:
    global _next_id
    task = payload.model_dump()
    task["id"] = _next_id
    _tasks[_next_id] = task
    _next_id += 1
    return dict(task)


def list_tasks() -> list[dict]:
    return [dict(v) for v in _tasks.values()]


def get_task(task_id: int) -> dict | None:
    task = _tasks.get(task_id)
    return dict(task) if task else None


def update_task(task_id: int, changes: dict) -> dict | None:
    if task_id not in _tasks:
        return None
    _tasks[task_id].update(changes)
    return dict(_tasks[task_id])


def delete_task(task_id: int) -> bool:
    return _tasks.pop(task_id, None) is not None
