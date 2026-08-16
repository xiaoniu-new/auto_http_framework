from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from common.config import (
    API_TOKEN,
    BASE_URL,
    DEFAULT_TIMEOUT,
    get_domain_config,
)


class HttpClient:
    """统一请求客户端，负责封装 base_url、超时、鉴权和通用请求参数。"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        domain: Optional[str] = None,
    ):
        # Domain-aware configuration (backwards compatible): if `domain` is
        # provided, load domain config and use its values unless explicit
        # arguments override them.
        domain_cfg: Optional[Dict[str, Any]] = None
        if domain:
            try:
                domain_cfg = get_domain_config(domain)
            except Exception:
                domain_cfg = None

        resolved_base = None
        resolved_token = None
        resolved_timeout = None
        resolved_headers: Dict[str, str] = {}
        resolved_common_params: Dict[str, Any] = {}

        if domain_cfg:
            resolved_base = domain_cfg.get("base_url")
            resolved_token = domain_cfg.get("api_token")
            resolved_timeout = domain_cfg.get("request_timeout")
            resolved_headers.update(domain_cfg.get("common_headers", {}) or {})
            resolved_common_params = domain_cfg.get("common_params", {}) or {}

        # explicit args override domain config
        if base_url is not None:
            resolved_base = base_url
        if token is not None:
            resolved_token = token
        if timeout is not None:
            resolved_timeout = timeout
        if headers:
            resolved_headers.update(headers)

        self.base_url = (resolved_base or BASE_URL).rstrip("/")
        self.timeout = resolved_timeout or DEFAULT_TIMEOUT
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.headers.update(resolved_headers)

        access_token = resolved_token if resolved_token is not None else API_TOKEN
        if access_token:
            self.headers["Authorization"] = f"Bearer {access_token}"

        # store common query params to be merged into each request
        self.common_params = resolved_common_params or {}

    def _build_url(self, path: str) -> str:
        if not path:
            return self.base_url
        prefix = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{prefix}"

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ):
        final_headers = dict(self.headers)
        if headers:
            final_headers.update(headers)

        # merge common params configured for the domain with per-request params
        final_params: Dict[str, Any] = {}
        final_params.update(self.common_params or {})
        if params:
            final_params.update(params)

        response = requests.request(
            method=method.upper(),
            url=self._build_url(path),
            params=final_params or None,
            json=json,
            data=data,
            headers=final_headers,
            timeout=timeout or self.timeout,
            **kwargs,
        )
        return response

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs):
        return self.request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs):
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs):
        return self.request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs):
        return self.request("PATCH", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)
