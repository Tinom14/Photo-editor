import uuid

from pydantic import BaseModel

class FilterParameters(BaseModel):
    name: str
    parameters: dict

class Task(BaseModel):
    id: uuid.UUID
    status: str = "in_progress"
    result: bytes = None
    file_data: bytes
    task_filter: FilterParameters