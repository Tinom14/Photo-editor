from sqlalchemy.orm import Mapped, mapped_column
import uuid

from shared.postgres_connection.postgres import Base

class Task(Base):
    __tablename__ = 'Task'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(default='in_progress')
    result: Mapped[bytes] = mapped_column(default=b'')