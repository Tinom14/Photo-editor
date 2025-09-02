from abc import ABC, abstractmethod

class AbstractTaskService(ABC):
    @abstractmethod
    async def process_task(self, message_body: bytes):
        pass