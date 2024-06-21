from datetime import datetime

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.configs.database import get_db
from app.domains.dto.dtos import TaskDTO, TaskCreateDTO, TaskUpdateDTO
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


@task_router.post("/", status_code=201, description="Busca todos as tarefas", response_model=TaskDTO)
def create(request: TaskCreateDTO,
           task_repo: TaskRepository = Depends(get_task_repo)):
    request.created_at = datetime.now()
    task_service = TaskService(task_repo)
    return task_service.create_task(request)


@task_router.get("/{task_id}", status_code=200, description="Busca uma tarefa pelo ID", response_model=TaskDTO)
def find_by_id(task_id: int, task_repo: TaskRepository = Depends(get_task_repo)):

    task_service = TaskService(task_repo)
    return task_service.read_task(task_id)


@task_router.get("/", status_code=200, description="Busca todos as tarefas", response_model=list[TaskDTO])
def find_all(task_repo: TaskRepository = Depends(get_task_repo)):

    task_service = TaskService(task_repo)
    return task_service.find_all()


@task_router.put("/{task_id}", status_code=200, description="Atualiza uma tarefa", response_model=TaskDTO)
def update(task_id: int, request: TaskUpdateDTO, task_repo: TaskRepository = Depends(get_task_repo)):

    task_service = TaskService(task_repo)
    return task_service.update_task(task_id, request)


@task_router.delete("/{task_id}", status_code=204, description="Deleta uma tarefa")
def delete(task_id: int, task_repo: TaskRepository = Depends(get_task_repo)):

    task_service = TaskService(task_repo)
    task_service.delete_task(task_id)
