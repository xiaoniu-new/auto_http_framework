from __future__ import annotations

from typing import Any, Iterable, Sequence


class AssertUtil:
    """通用断言工具，不允许在业务用例中直接使用原生 assert。"""

    @staticmethod
    def assert_status_code(response, expected_code: int):
        if response is None:
            raise AssertionError("response对象不能为空")
        actual = getattr(response, "status_code", None)
        if actual != expected_code:
            raise AssertionError(f"status_code断言失败，期望={expected_code}，实际={actual}, body={response.text}")

    @staticmethod
    def assert_response_code(response, expected_code: int, message: str = "response code"):
        if not hasattr(response, "json"):
            raise AssertionError(f"{message}: response不包含json()")
        payload = response.json()
        actual = payload.get("code") if isinstance(payload, dict) else None
        if actual != expected_code:
            raise AssertionError(f"{message}: 期望code={expected_code}，实际={actual}，payload={payload}")

    @staticmethod
    def assert_field_exists(data: Any, field_name: str, parent_name: str = "payload"):
        if not isinstance(data, dict) or field_name not in data:
            raise AssertionError(f"{parent_name}中缺少字段: {field_name}")

    @staticmethod
    def assert_not_empty(value: Any, field_name: str):
        if value is None or value == "":
            raise AssertionError(f"字段 {field_name} 为空")

    @staticmethod
    def assert_number_ge_zero(value: Any, field_name: str):
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            raise AssertionError(f"字段 {field_name} 不是数字: {value}")
        if numeric < 0:
            raise AssertionError(f"字段 {field_name} 不能小于0: {value}")

    @staticmethod
    def assert_type(value: Any, expected_types: Sequence[type], field_name: str):
        if not isinstance(value, tuple(expected_types)):
            raise AssertionError(f"字段 {field_name} 类型不匹配，期望={expected_types}，实际={type(value).__name__}")

    @staticmethod
    def assert_in(value: Any, allowed_values: Iterable[Any], field_name: str):
        if value not in allowed_values:
            raise AssertionError(f"字段 {field_name} 值不在允许范围内: value={value}, allowed={list(allowed_values)}")
