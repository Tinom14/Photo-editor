from fastapi import Depends

from http_service.src.repository.abstract_user_repository import AbstractUserRepository
from http_service.src.repository.postgres.user_repository import UserRepository
from http_service.src.usecases.abstract_user_service import AbstractUserService
from http_service.src.usecases.service.user_service import UserService

from sqlalchemy.ext.asyncio import AsyncSession
from shared.postgres_connection.postgres import get_db

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> AbstractUserRepository:
    return UserRepository(db)

async def get_user_service(
    users_repo: AbstractUserRepository = Depends(get_user_repo)
) -> AbstractUserService:
    return UserService(users_repo)