import pytest

from common.assert_util import AssertUtil
from common.config import Config


pytestmark = pytest.mark.skipif(
    not Config.get_bool("ENABLE_LIVE_API", False),
    reason="Live API is disabled; set ENABLE_LIVE_API=true and provide API_BASE_URL to run this module.",
)


class TestLeaveApi:
    """假期管理接口专项用例。"""

    @pytest.mark.api
    def test_get_leave_balance_success(self, api_client):
        """场景：用户查询假期余额成功。"""
        response = api_client.get("/hr/leave/balance", params={"user_id": "10001"})
        AssertUtil.assert_status_code(response, 200)
        AssertUtil.assert_response_code(response, 0, "查询假期余额")

        payload = response.json()
        AssertUtil.assert_field_exists(payload, "data")
        data = payload.get("data")
        AssertUtil.assert_field_exists(data, "user_id")
        AssertUtil.assert_field_exists(data, "leave_balance")
        AssertUtil.assert_number_ge_zero(data.get("leave_balance"), "leave_balance")

    @pytest.mark.parametrize(
        "params, expected_status, expected_code",
        [
            ({"user_id": ""}, 400, 1001),
            ({"user_id": None}, 400, 1001),
            ({}, 400, 1001),
        ],
    )
    @pytest.mark.api
    def test_get_leave_balance_invalid_params(self, api_client, params, expected_status, expected_code):
        """场景：查询假期余额时传入非法参数，返回错误信息。"""
        response = api_client.get("/hr/leave/balance", params=params)
        AssertUtil.assert_status_code(response, expected_status)
        AssertUtil.assert_response_code(response, expected_code, "查询假期余额-非法参数")

        payload = response.json()
        AssertUtil.assert_field_exists(payload, "message")
        AssertUtil.assert_not_empty(payload.get("message"), "message")

    @pytest.mark.parametrize(
        "body, expected_status, expected_code",
        [
            ({"user_id": "10001", "leave_type": "", "days": 1}, 400, 1002),
            ({"user_id": "10001", "leave_type": "annual", "days": -1}, 400, 1002),
            ({"user_id": "10001", "leave_type": "annual", "days": "abc"}, 400, 1002),
        ],
    )
    @pytest.mark.api
    def test_apply_leave_invalid_request(self, api_client, body, expected_status, expected_code):
        """场景：提交请假申请时参数异常，返回校验错误。"""
        response = api_client.post("/hr/leave/apply", json=body)
        AssertUtil.assert_status_code(response, expected_status)
        AssertUtil.assert_response_code(response, expected_code, "提交请假申请-非法参数")

        payload = response.json()
        AssertUtil.assert_field_exists(payload, "message")
        AssertUtil.assert_not_empty(payload.get("message"), "message")
