from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
import yaml
from pathlib import Path


def load_config():
    config_path = Path("shared/postgres_connection/config.yml")
    if not config_path.exists():
        raise FileNotFoundError("Config file config.yml not found")

    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


config = load_config()
postgres_config = config.get('postgres', {})

database_url = (
    f"postgresql+asyncpg://"
    f"{postgres_config.get('user', 'postgres')}:"
    f"{postgres_config.get('password', 'postgres')}@"
    f"{postgres_config.get('host', 'db')}:"
    f"{postgres_config.get('port', 5432)}/"
    f"{postgres_config.get('dbname', 'app_db')}"
)

engine = create_async_engine(database_url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)