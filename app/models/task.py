from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: Enum('Status', ['Pendente', 'Em progresso', 'Concluída'])
    created_at: datetime
