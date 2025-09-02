from abc import ABC, abstractmethod
import uuid
from shared.schemas.schemas import Task


class AbstractTaskRepository(ABC):
    @abstractmethod
    async def create_task(self, task_id: uuid.UUID) -> Task:
        pass

    @abstractmethod
    async def get_task(self, task_id: uuid.UUID) -> Task:
        pass