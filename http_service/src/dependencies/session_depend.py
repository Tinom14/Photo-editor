from fastapi import Depends
from http_service.src.repository.redis.session_repository import SessionRepository
from http_service.src.repository.abstract_session_repository import AbstractSessionRepository
from http_service.src.usecases.abstract_session_service import AbstractSessionService
from http_service.src.usecases.service.session_service import SessionService
import shared.redis_connection.config as redis_config_module


async def get_session_repo() -> AbstractSessionRepository:
    if redis_config_module.redis_client is None:
        raise RuntimeError("Redis клиент не инициализирован")
    return SessionRepository(redis_config_module.redis_client)

async def get_session_service(
    sessions_repo: AbstractSessionRepository = Depends(get_session_repo)
) -> AbstractSessionService:
    return SessionService(sessions_repo)
