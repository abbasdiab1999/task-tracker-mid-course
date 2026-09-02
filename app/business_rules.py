from __future__ import annotations
from datetime import date
from .models import TaskStatus

ALLOWED_TRANSITIONS = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.TODO, TaskStatus.DONE},
    TaskStatus.DONE: {TaskStatus.IN_PROGRESS},
}


def validate_status_transition(current: TaskStatus, requested: TaskStatus) -> None:
    if requested == current:
        return
    if requested not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"Invalid status transition: {current.value} -> {requested.value}")


def is_overdue(task: dict) -> bool:
    due = task.get("due_date")
    if not due:
        return False
    return due < date.today() and task.get("status") != TaskStatus.DONE
