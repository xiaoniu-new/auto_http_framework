from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from common.config import API_TOKEN, BASE_URL, DEFAULT_TIMEOUT


class HttpClient:
    """统一请求客户端，负责封装 base_url、超时、鉴权和通用请求参数。"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if headers:
            self.headers.update(headers)

        access_token = token if token is not None else API_TOKEN
        if access_token:
            self.headers["Authorization"] = f"Bearer {access_token}"

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

        response = requests.request(
            method=method.upper(),
            url=self._build_url(path),
            params=params,
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
