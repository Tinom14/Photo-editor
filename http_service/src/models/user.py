from sqlalchemy.orm import Mapped, mapped_column

from shared.postgres_connection.postgres import Base

class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]