from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert
from app.schemas import CreateUser, UpdateUser

from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/user_id")
async def get_user_by_id(db: Annotated[Session,Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.post("/create")
async def create_user(db: Annotated[Session,Depends(get_db)], create_user_model: CreateUser):
    db.execute(insert(User).values(
        username=create_user_model.username,
        firstname=create_user_model.firstname,
        lastname=create_user_model.lastname,
        age=create_user_model.age,
        slug=slugify(create_user_model.username)))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user_model: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user_model.firstname,
        lastname=update_user_model.lastname,
        age=update_user_model.age,
        slug=slugify(update_user_model.username)
    ))

    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}

@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(update(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
