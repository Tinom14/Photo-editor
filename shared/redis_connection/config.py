from pydantic import BaseModel
import yaml
from pathlib import Path
import redis.asyncio as redis

class RedisConnectionConfig(BaseModel):
    host: str
    port: int
    password: str | None = None
    db: int

def load_redis_config(file_path: Path = Path("shared/redis_connection/config.yml")) -> RedisConnectionConfig:
    with open(file_path) as f:
        config_data = yaml.safe_load(f)
    return RedisConnectionConfig(**config_data["redis"])

redis_config = load_redis_config()

redis_client: redis.Redis | None = None
