from abc import ABC, abstractmethod
from http_service.src.models.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_user(self, login: str, hashed_password: str) -> User:
        pass

    @abstractmethod
    async def get_user(self, login: str) -> User:
        pass