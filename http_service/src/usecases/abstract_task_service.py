import uuid
from abc import ABC, abstractmethod
from shared.schemas.schemas import FilterParameters

class AbstractTaskService(ABC):
    @abstractmethod
    async def create_task(self, image_data: bytes, task_filter: FilterParameters) -> uuid.UUID:
        pass

    @abstractmethod
    async def get_task_status(self, task_id: uuid.UUID) -> str:
        pass

    @abstractmethod
    async def get_task_result(self, task_id: uuid.UUID) -> bytes:
        pass