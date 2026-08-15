import pytest

from common.assert_util import AssertUtil
from common.config import Config


pytestmark = pytest.mark.skipif(
    not Config.get_bool("ENABLE_LIVE_API", False),
    reason="Live API is disabled; set ENABLE_LIVE_API=true and provide API_BASE_URL to run this module.",
)


class TestSalaryApi:
    """薪酬管理接口专项用例。"""

    @pytest.mark.api
    @pytest.mark.parametrize(
        "params",
        [{"user_id": "10001"}, {"user_id": ""}, {"user_id": None}, {}],
    )
    def test_get_salary_detail(self, api_client, params):
        """场景：查询薪酬明细，校验成功与异常参数。"""
        response = api_client.get("/hr/salary/detail", params=params)
        if params.get("user_id") in {"10001"}:
            AssertUtil.assert_status_code(response, 200)
            AssertUtil.assert_response_code(response, 0, "查询薪酬明细")
        else:
            AssertUtil.assert_status_code(response, 400)
            AssertUtil.assert_response_code(response, 1001, "查询薪酬明细-非法参数")
