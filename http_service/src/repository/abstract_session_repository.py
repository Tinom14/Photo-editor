from abc import ABC, abstractmethod
from http_service.src.schemas.schemas import Session


class AbstractSessionRepository(ABC):
    @abstractmethod
    async def create_session(self, user_id: int, session_id: str):
        pass

    @abstractmethod
    async def get_session(self, session_id: str) -> Session:
        pass