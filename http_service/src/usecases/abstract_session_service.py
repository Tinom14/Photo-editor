from abc import ABC, abstractmethod
from http_service.src.schemas.schemas import Session

class AbstractSessionService(ABC):
    @abstractmethod
    async def create_session(self, user_id: int) -> str:
        pass

    @abstractmethod
    async def get_session(self, session_id: str) -> Session:
        pass
