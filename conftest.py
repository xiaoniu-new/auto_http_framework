import pytest

from common.config import DEFAULT_DOMAIN, get_domain_config, ENABLE_LIVE_API
from common.http_client import HttpClient


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: smoke test")
    config.addinivalue_line("markers", "api: http interface test")


def pytest_addoption(parser):
    parser.addoption(
        "--product-line",
        action="store",
        default=DEFAULT_DOMAIN,
        help="Business domain to run tests for (e.g. hr, finance)",
    )


@pytest.fixture(scope="session")
def product_line(request):
    return request.config.getoption("--product-line")


@pytest.fixture(scope="session")
def domain_config(product_line):
    """Return merged domain configuration dict for the requested product line."""
    if not product_line:
        raise RuntimeError("No product line specified. Use --product-line or set PRODUCT_LINE env var.")
    return get_domain_config(product_line)


@pytest.fixture(scope="session")
def api_client(domain_config):
    """Create an HttpClient instance configured for the specific domain.

    This avoids changing the low-level `common.http_client.HttpClient` implementation.
    """
    return HttpClient(
        base_url=domain_config.get("base_url"),
        token=domain_config.get("api_token"),
        timeout=domain_config.get("request_timeout"),
        headers=domain_config.get("common_headers"),
    )


@pytest.fixture(scope="session")
def auth_headers(domain_config):
    token = domain_config.get("api_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def live_api_enabled():
    return ENABLE_LIVE_API
