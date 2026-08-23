from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskBase(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        seen = set()
        for item in values:
            tag = item.strip()
            if not tag:
                raise ValueError("tags must not be blank")
            if len(tag) > 30:
                raise ValueError("each tag must be at most 30 characters")
            key = tag.lower()
            if key not in seen:
                seen.add(key)
                cleaned.append(tag)
        return cleaned


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, values: Optional[list[str]]) -> Optional[list[str]]:
        if values is None:
            return values
        cleaned: list[str] = []
        seen = set()
        for item in values:
            tag = item.strip()
            if not tag:
                raise ValueError("tags must not be blank")
            if len(tag) > 30:
                raise ValueError("each tag must be at most 30 characters")
            key = tag.lower()
            if key not in seen:
                seen.add(key)
                cleaned.append(tag)
        return cleaned


class TaskResponse(TaskBase):
    id: int
    overdue: bool
