from http_service.src.schemas.exceptions import InvalidCredentialsError
from http_service.src.usecases.abstract_user_service import AbstractUserService
from http_service.src.repository.abstract_user_repository import AbstractUserRepository
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserService(AbstractUserService):
    def __init__(self, users_repo: AbstractUserRepository):
        self.users_repo: AbstractUserRepository = users_repo

    async def create_user(self, login: str, password: str) -> int:
        hashed_password = bcrypt_context.hash(password)
        user = await self.users_repo.create_user(login, hashed_password)
        return user.id

    async def login_user(self, login: str, password: str) -> int:
        user = await self.users_repo.get_user(login)
        if not bcrypt_context.verify(password, user.password):
            raise InvalidCredentialsError("Invalid password")
        return user.id
