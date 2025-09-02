import os
from pydantic import BaseModel
import yaml
import argparse
import logging


class HTTPConfig(BaseModel):
    address: str


class AppConfig:
    @staticmethod
    def parse_flags() -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", help="Path to config file", default="")
        parser.add_argument("--host", help="Server host", default=None)
        parser.add_argument("--port", help="Server port", type=int, default=None)
        return parser.parse_args()

    @staticmethod
    def must_load(cfg_path: str) -> HTTPConfig:
        if not cfg_path:
            logging.error("Config path is not set")
            raise ValueError("Config path is not set")

        if not os.path.exists(cfg_path):
            logging.error(f"Config file does not exist: {cfg_path}")
            raise FileNotFoundError(f"Config file does not exist: {cfg_path}")

        with open(cfg_path, 'r') as f:
            config_data = yaml.safe_load(f)

        try:
            return HTTPConfig(**config_data)
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            raise