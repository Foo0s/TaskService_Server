from typing import List, Dict, Union

from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.tasks import TaskSchemaAdd, TaskSchemaEdit
from src.services.tasks import TasksService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("")
async def get_tasks(uow: UOWDep):
    tasks = await TasksService().get_tasks(uow)
    return tasks


@router.get("/history")
async def get_task_history(uow: UOWDep):
    tasks = await TasksService().get_task_history(uow)
    return tasks


@router.post("")
async def add_task(task: TaskSchemaAdd, uow: UOWDep):
    task_id = await TasksService().add_task(uow, task)
    return {"task_id": task_id}


@router.patch("/{task_id}")
async def edit_task(task_id: int, task: TaskSchemaEdit, uow: UOWDep):
    task_id = await TasksService().edit_task(uow, task_id, task)
    return {"task_id": task_id}


@router.delete("/{task_id}")
async def delete_task(task_id: int, uow: UOWDep):
    result = await TasksService().delete_task(uow, task_id)
    return {"deleted_row": result}
