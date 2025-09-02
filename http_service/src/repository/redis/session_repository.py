from http_service.src.repository.abstract_session_repository import AbstractSessionRepository
from http_service.src.schemas.schemas import Session
from http_service.src.schemas.exceptions import NotFoundError
import redis.asyncio as redis


class SessionRepository(AbstractSessionRepository):
    def __init__(self, redis_client: redis.Redis):
        self.client = redis_client

    async def create_session(self, user_id: int, session_id: str):
        await self.client.set(session_id, user_id)

    async def get_session(self, session_id: str) -> Session:
        session = await self.client.get(session_id)
        if session is None:
            raise NotFoundError(f"Session {session_id} not found")
        return Session(user_id=int(session.decode()), session_id=session_id)