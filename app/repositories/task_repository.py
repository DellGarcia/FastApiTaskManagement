from sqlalchemy.orm import Session

from app.domains.models.task_model import TaskModel


class ITaskRepository:
    def create(self, task: object):
        raise NotImplementedError

    def read(self, task_id: int):
        raise NotImplementedError

    def update(self, task: object, task_data: dict):
        raise NotImplementedError

    def delete(self, task: object):
        raise NotImplementedError

    def find_all(self):
        raise NotImplementedError


class TaskRepository(ITaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: TaskModel) -> TaskModel:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task: TaskModel, task_data) -> TaskModel:
        for key, value in task_data.items():
            setattr(task, key, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: TaskModel) -> int:
        task_id = task.id
        self.session.delete(task)
        self.session.commit()
        return task_id

    def read(self, task_id):
        return self.session.query(TaskModel).filter(TaskModel.id == task_id).first()

    def find_all(self):
        return self.session.query(TaskModel).all()
