import pytest

from common.config import API_TOKEN, BASE_URL, ENABLE_LIVE_API
from common.http_client import HttpClient


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: smoke test")
    config.addinivalue_line("markers", "api: http interface test")


@pytest.fixture(scope="session")
def api_client():
    """统一的 HTTP 请求客户端，默认通过配置项读取基础信息。"""
    return HttpClient(base_url=BASE_URL, token=API_TOKEN)


@pytest.fixture(scope="session")
def auth_headers():
    """返回通用鉴权头信息。"""
    if not API_TOKEN:
        return {}
    return {"Authorization": f"Bearer {API_TOKEN}"}


@pytest.fixture(scope="session")
def live_api_enabled():
    return ENABLE_LIVE_API
