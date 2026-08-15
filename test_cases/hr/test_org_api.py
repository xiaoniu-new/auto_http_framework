import pytest

from common.assert_util import AssertUtil
from common.config import Config


pytestmark = pytest.mark.skipif(
    not Config.get_bool("ENABLE_LIVE_API", False),
    reason="Live API is disabled; set ENABLE_LIVE_API=true and provide API_BASE_URL to run this module.",
)


class TestOrganizationApi:
    """组织架构接口专项用例。"""

    @pytest.mark.api
    @pytest.mark.parametrize(
        "params",
        [{"department_id": "D001"}, {"department_id": ""}, {"department_id": None}, {}],
    )
    def test_get_organization_members(self, api_client, params):
        """场景：查询组织成员列表，覆盖正常与非法参数。"""
        response = api_client.get("/hr/organization/members", params=params)
        if params.get("department_id") == "D001":
            AssertUtil.assert_status_code(response, 200)
            AssertUtil.assert_response_code(response, 0, "查询组织成员")
        else:
            AssertUtil.assert_status_code(response, 400)
            AssertUtil.assert_response_code(response, 1001, "查询组织成员-非法参数")
