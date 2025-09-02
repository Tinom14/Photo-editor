from abc import ABC, abstractmethod
import uuid

class TaskSender(ABC):
    @abstractmethod
    async def send_task(self, task_id: uuid.UUID, image_data: bytes, filter_obj: dict):
        pass
