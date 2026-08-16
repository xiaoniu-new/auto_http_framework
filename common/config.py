import os
from pathlib import Path
from typing import Any, Dict

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "datas" / "config"
COMMON_CONFIG_PATH = CONFIG_DIR / "common.yaml"

# Default domain (业务域) can be set via env PRODUCT_LINE
DEFAULT_DOMAIN = os.getenv("PRODUCT_LINE", "").strip() or None


def _load_yaml_file(path: Path) -> Dict[str, Any]:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            if isinstance(data, dict):
                return data
    return {}


def get_domain_config(domain: str) -> Dict[str, Any]:
    """Load and return merged configuration for a business domain.

    Merge order: common.yaml <- {domain}.yaml (domain overrides common).
    Returned dict contains keys: base_url, api_token, request_timeout,
    common_headers, common_params (all optional).
    """
    if not domain:
        raise ValueError("domain must be provided")

    common = _load_yaml_file(COMMON_CONFIG_PATH)
    domain_path = CONFIG_DIR / f"{domain}.yaml"
    domain_cfg = _load_yaml_file(domain_path)

    merged = dict(common)
    merged.update(domain_cfg)

    # normalize keys
    if "base_url" in merged and isinstance(merged["base_url"], str):
        merged["base_url"] = merged["base_url"].rstrip("/")
    merged.setdefault("api_token", "")
    merged.setdefault("request_timeout", common.get("request_timeout", 10))
    merged.setdefault("common_headers", common.get("common_headers", {}) or {})
    merged.setdefault("common_params", common.get("common_params", {}) or {})

    return merged


class Config:
    """兼容性的配置读取入口。用于读取全局/通用配置和环境变量。

    Note: domain-specific configuration should be read with `get_domain_config`.
    """

    @staticmethod
    def _load_common() -> Dict[str, Any]:
        return _load_yaml_file(COMMON_CONFIG_PATH)

    @classmethod
    def get(cls, key: str, default=None):
        # environment override
        value = os.getenv(key)
        if value is not None:
            return value
        data = cls._load_common()
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


# Backwards-compatible module-level defaults: if PRODUCT_LINE set, derive
# API_* values from that domain; otherwise fall back to common.yaml top-level.
if DEFAULT_DOMAIN:
    _domain_cfg = get_domain_config(DEFAULT_DOMAIN)
    API_BASE_URL = _domain_cfg.get("base_url", "http://127.0.0.1:8000")
    API_TOKEN = _domain_cfg.get("api_token", "")
    DEFAULT_TIMEOUT = int(_domain_cfg.get("request_timeout", 10))
else:
    API_BASE_URL = Config.get("API_BASE_URL", "http://127.0.0.1:8000")
    API_TOKEN = Config.get("API_TOKEN", "")
    DEFAULT_TIMEOUT = Config.get_int("API_TIMEOUT", 10)

BASE_URL = API_BASE_URL.rstrip("/")
ENABLE_LIVE_API = Config.get_bool("ENABLE_LIVE_API", False)
