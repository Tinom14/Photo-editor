from pydantic import BaseModel
import yaml
from pathlib import Path


class RabbitConnectionConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    queue: str


def load_rabbitmq_config(file_path: Path = Path("shared/rabbit_connection/config.yml")) -> RabbitConnectionConfig:
    with open(file_path) as f:
        config_data = yaml.safe_load(f)
    return RabbitConnectionConfig(**config_data["rabbit_mq"])


rabbitmq_config = load_rabbitmq_config()
