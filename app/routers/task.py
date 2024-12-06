from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert
from app.schemas import CreateUser, CreateTask

from slugify import slugify
from sqlalchemy import select
from sqlalchemy import update

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def get_all_tasks():
    pass
@router.get("/task_id")
async def get_task_by_id():
    pass
@router.post("/create")
async def create_task():
    pass

@router.post("/update")
async def update_task():
    pass
@router.delete("/delete")
async def delete_task():
    pass
