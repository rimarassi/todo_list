from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from authentication.api import get_current_user
from categories.models import Category
from .models import Task


router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: Literal['pending', 'in_progress', 'completed'] = 'pending'
    priority: Literal['low', 'medium', 'high'] = 'medium'
    due_date: date | None = None
    category_id: int | None = None


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    status: str = 'pending'
    priority: str = 'medium'
    due_date: date | None = None
    category_id: int | None = None


@router.get('/')
def task_list(current_user=Depends(get_current_user)):
    tasks = Task.objects.filter(user=current_user)

    return list(tasks.values(
        'id',
        'title',
        'description',
        'status',
        'priority',
        'due_date',
        'created_at',
        'updated_at',
        'completed_at',
        'category_id'
    ))


@router.post('/', status_code=status.HTTP_201_CREATED)
def task_create(
    data: TaskCreate,
    current_user=Depends(get_current_user)
):
    category = None

    if data.category_id is not None:
        category = Category.objects.filter(
            id=data.category_id,
            user=current_user
        ).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Categoria não encontrada.'
            )

    task = Task.objects.create(
        user=current_user,
        category=category,
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        due_date=data.due_date
    )

    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'due_date': task.due_date,
        'created_at': task.created_at,
        'updated_at': task.updated_at,
        'completed_at': task.completed_at,
        'category_id': task.category_id
    }


@router.put('/{task_id}')
def task_update(
    task_id: int,
    data: TaskUpdate,
    current_user=Depends(get_current_user)
):
    task = Task.objects.filter(
        id=task_id,
        user=current_user
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tarefa não encontrada.'
        )

    category = None

    if data.category_id is not None:
        category = Category.objects.filter(
            id=data.category_id,
            user=current_user
        ).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Categoria não encontrada.'
            )

    task.title = data.title
    task.description = data.description
    task.status = data.status
    task.priority = data.priority
    task.due_date = data.due_date
    task.category = category

    task.save()

    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'due_date': task.due_date,
        'created_at': task.created_at,
        'updated_at': task.updated_at,
        'completed_at': task.completed_at,
        'category_id': task.category_id
    }


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def task_delete(
    task_id: int,
    current_user=Depends(get_current_user)
):
    task = Task.objects.filter(
        id=task_id,
        user=current_user
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tarefa não encontrada.'
        )

    task.delete()
