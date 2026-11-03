from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from authentication.api import get_current_user
from .models import Category


router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)


class CategoryCreate(BaseModel):
    name: str
    color: str = '#808080'


class CategoryUpdate(BaseModel):
    name: str
    color: str = '#808080'


@router.get('/')
def category_list(current_user=Depends(get_current_user)):
    categories = Category.objects.filter(user=current_user)

    return list(categories.values(
        'id',
        'name',
        'color',
        'created_at'
    ))


@router.post('/', status_code=status.HTTP_201_CREATED)
def category_create(
    data: CategoryCreate,
    current_user=Depends(get_current_user)
):
    category = Category.objects.create(
        user=current_user,
        name=data.name,
        color=data.color
    )

    return {
        'id': category.id,
        'name': category.name,
        'color': category.color,
        'created_at': category.created_at
    }


@router.put('/{category_id}')
def category_update(
    category_id: int,
    data: CategoryUpdate,
    current_user=Depends(get_current_user)
):
    category = Category.objects.filter(
        id=category_id,
        user=current_user
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Categoria não encontrada.'
        )

    category.name = data.name
    category.color = data.color
    category.save()

    return {
        'id': category.id,
        'name': category.name,
        'color': category.color,
        'created_at': category.created_at
    }


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def category_delete(
    category_id: int,
    current_user=Depends(get_current_user)
):
    category = Category.objects.filter(
        id=category_id,
        user=current_user
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Categoria não encontrada.'
        )

    category.delete()
