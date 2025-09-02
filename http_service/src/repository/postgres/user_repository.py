from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from http_service.src.repository.abstract_user_repository import AbstractUserRepository
from http_service.src.models.user import User
from http_service.src.schemas.exceptions import NotFoundError, LoginAlreadyExistsError, DatabaseError


class UserRepository(AbstractUserRepository):
    def __init__(self, db):
        self.db = db

    async def create_user(self, login: str, hashed_password: str) -> User:
        try:
            await self.db.execute(insert(User).values(username=login, password=hashed_password))
            await self.db.commit()

            user = await self.get_user(login)
            return user

        except IntegrityError as e:
            await self.db.rollback()
            if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                raise LoginAlreadyExistsError(f"Login '{login}' already exists")
            else:
                raise DatabaseError(f"Database integrity error: {e}")

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseError(f"Database error: {e}")

        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"Unexpected error: {e}")

    async def get_user(self, login: str) -> User:
        try:
            user = await self.db.scalar(
                select(User).where(User.username == login)
            )
            if user is None:
                raise NotFoundError(f"Login {login} not found")
            return user

        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while fetching user: {e}")
