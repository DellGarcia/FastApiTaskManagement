from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict


class Validate:
    @classmethod
    def status(cls, status):
        possible_status = ["Pendente", "Em Progresso", "Concluída"]

        if status not in possible_status:
            raise ValueError('Status must be one of {}'.format(possible_status))
        return status


class TaskDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: str
    created_at: datetime


class TaskCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    title: str
    description: str
    status: str
    created_at: datetime

    @field_validator('status')
    def validate_status(cls, status):
        return Validate.status(status)


class TaskUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    title: str
    description: str
    status: str
    created_at: datetime

    @field_validator('status')
    def validate_status(cls, status):
        return Validate.status(status)
