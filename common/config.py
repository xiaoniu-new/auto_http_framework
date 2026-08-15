import os
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / "datas" / "config.yaml"


class Config:
    """统一配置读取入口。优先读取环境变量，其次回退到 datas/config.yaml。"""

    @staticmethod
    def _load_yaml_file() -> dict:
        if DEFAULT_CONFIG_PATH.exists():
            with DEFAULT_CONFIG_PATH.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or {}
                if isinstance(data, dict):
                    return data
        return {}

    @classmethod
    def get(cls, key: str, default=None):
        value = os.getenv(key)
        if value is not None:
            return value
        data = cls._load_yaml_file()
        return data.get(key, default)

    @classmethod
    def get_int(cls, key: str, default: int = 0) -> int:
        value = cls.get(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def get_bool(cls, key: str, default: bool = False) -> bool:
        value = cls.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "y", "on"}
        return bool(value)


API_BASE_URL = Config.get("API_BASE_URL", "http://127.0.0.1:8000")
BASE_URL = API_BASE_URL.rstrip("/")
DEFAULT_TIMEOUT = Config.get_int("API_TIMEOUT", 10)
API_TOKEN = Config.get("API_TOKEN", "")
ENABLE_LIVE_API = Config.get_bool("ENABLE_LIVE_API", False)
