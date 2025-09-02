from abc import ABC, abstractmethod

class AbstractUserService(ABC):
    @abstractmethod
    async def create_user(self, login: str, password: str) -> int:
        pass

    @abstractmethod
    async def login_user(self, login: str, password: str) -> int:
        pass

