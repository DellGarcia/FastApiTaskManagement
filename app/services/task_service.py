import logging

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from app.domains.dto.dtos import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from app.domains.models.task_model import TaskModel
from app.repositories.task_repository import ITaskRepository

logger = logging.getLogger("fastapi")


class ITaskService:

    def create_user(self, user_data: object):
        raise NotImplementedError

    def read_user(self, user_id: int):
        raise NotImplementedError

    def update_user(self, user_id: int, user_update: object):
        raise NotImplementedError

    def delete_user(self, user_id: int):
        raise NotImplementedError


class TaskService(ITaskService):

    def __init__(self, user_repository: ITaskRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: TaskCreateDTO) -> TaskDTO:
        user = TaskModel(**user_data.model_dump())
        try:
            logger.info("Creating user: %s", user)
            created_user = self.user_repository.create(user)
        except IntegrityError as e:
            logger.error("Error creating user: %s. Detail: %s", user, e)
            raise HTTPException(status_code=409, detail=f"Task already exists. Error: {e.args[0]}")
        return TypeAdapter(TaskDTO).validate_python(created_user)

    def read_user(self, user_id: int) -> TaskDTO:
        logger.info("Reading user with id %s", user_id)
        user = self.user_repository.read(user_id)
        if user is None:
            logger.error("TaskModel with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="Task not found")
        return TypeAdapter(TaskDTO).validate_python(user)

    def find_all(self) -> list[TaskDTO]:
        logger.info("Finding all users")
        users = self.user_repository.find_all()
        return [TypeAdapter(TaskDTO).validate_python(user) for user in users]

    def update_user(self, user_id: int, user_data: TaskUpdateDTO) -> TaskDTO:
        logger.info("Updating user with id %s", user_id)
        user = self.user_repository.read(user_id)
        if user is None:
            logger.error("Task with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="TaskModel not found")
        user_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        updated_user = self.user_repository.update(user, user_data)
        return TypeAdapter(TaskDTO).validate_python(updated_user)

    def delete_user(self, user_id: int) -> int:
        logger.info("Deleting user with id %s", user_id)
        user = self.user_repository.read(user_id)
        if user is None:
            logger.error("Task with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="TaskModel not found")
        delete_id = self.user_repository.delete(user)
        return delete_id
