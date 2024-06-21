from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional


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
    created_at: Optional[datetime]

    @field_validator('status')
    def validate_status(cls, status):
        return Validate.status(status)


class TaskCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    status: str
    created_at: Optional[datetime] = None

    @field_validator('status')
    def validate_status(cls, status):
        return Validate.status(status)


class TaskUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    @field_validator('status')
    def validate_status(cls, status):
        return Validate.status(status)
