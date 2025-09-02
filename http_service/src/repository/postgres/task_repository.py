from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
import uuid

from http_service.src.repository.abstract_task_repository import AbstractTaskRepository
from http_service.src.schemas.exceptions import NotFoundError, DatabaseError
from shared.postgres_connection.models.task import Task


class TaskRepository(AbstractTaskRepository):
    def __init__(self, db):
        self.db = db

    async def create_task(self, task_id: uuid.UUID) -> Task:
        try:
            await self.db.execute(insert(Task).values(id=task_id))
            await self.db.commit()

            task = await self.get_task(task_id)
            return task

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseError(f"Database error: {e}")

        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"Unexpected error: {e}")


    async def get_task(self, task_id: uuid.UUID) -> Task:
        try:
            task = await self.db.scalar(
                select(Task).where(Task.id == task_id)
            )
            if task is None:
                raise NotFoundError(f"Task {task_id} not found")
            return task

        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error while fetching user: {e}")