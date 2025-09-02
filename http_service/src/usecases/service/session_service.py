from http_service.src.schemas.schemas import Session
from http_service.src.usecases.abstract_session_service import AbstractSessionService
from http_service.src.repository.abstract_session_repository import AbstractSessionRepository
from passlib.context import CryptContext
import secrets

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class SessionService(AbstractSessionService):
    def __init__(self, sessions_repo: AbstractSessionRepository):
        self.sessions_repo: AbstractSessionRepository = sessions_repo

    async def create_session(self, user_id: int) -> str:
        token = secrets.token_urlsafe(32)
        await self.sessions_repo.create_session(user_id, token)
        return token

    async def get_session(self, session_id: str) -> Session:
        session = await self.sessions_repo.get_session(session_id)
        return session

