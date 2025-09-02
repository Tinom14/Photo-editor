from abc import ABC, abstractmethod
from shared.schemas.schemas import Task
import uuid


class AbstractTaskSender(ABC):
    @abstractmethod
    async def save_result(self, task_id: uuid.UUID, image_data: bytes) -> Task:
        pass